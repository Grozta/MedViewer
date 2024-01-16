import os

import torch
import torch.nn as nn
from torchvision import models
from torchvision.models.vgg import make_layers, VGG, cfgs

from util import get_base_dir

base_dir = get_base_dir()


class MRNet(nn.Module):
    def __init__(self):
        super().__init__()
        self.model = models.alexnet(pretrained=True)
        self.gap = nn.AdaptiveAvgPool2d(1)
        self.classifier = nn.Linear(256, 1)

    def forward(self, x):
        x = torch.squeeze(x, dim=0)  # only batch size 1 supported
        x = self.model.features(x)
        x = self.gap(x).view(x.size(0), -1)
        x = torch.max(x, 0, keepdim=True)[0]
        x = self.classifier(x)
        return x


class TripleMRNet(nn.Module):
    def __init__(self, backbone="vgg16", training=True):
        super().__init__()
        self.backbone = backbone
        if self.backbone == "vgg16":
            model = VGG(make_layers(cfgs['D'], batch_norm=False), **{'init_weights': False})
            state_dict = torch.load(os.path.join(base_dir, 'models/classify', 'vgg16-397923af.pth'))
            model.load_state_dict(state_dict)
            vgg16featuremap = model.features
            # vgg16featuremap = models.vgg16(pretrained=True).features
            self.net = vgg16featuremap
            for param in self.net.parameters():
                param.requires_grad = True  # 屏蔽预训练模型权重，权重和偏置值不更新，只训练全连接层的权重

        if self.backbone == "resnet18":
            resnet = models.resnet18(pretrained=training)
            modules = list(resnet.children())[:-1]
            self.net = nn.Sequential(*modules)
            for param in self.axial_net.parameters():
                param.requires_grad = False
        elif self.backbone == "alexnet":
            self.net = models.alexnet(pretrained=training)

        self.gap = nn.AdaptiveAvgPool2d(1)

        if self.backbone == "resnet18":
            self.classifier = nn.Linear(3 * 512, 1)
        elif self.backbone == "alexnet":
            self.classifier = nn.Linear(3 * 256, 1)
        elif self.backbone == "vgg16":
            self.classifier = nn.Linear(512, 1)

    def forward(self, x):
        if x.shape[0] != 1:
            input = torch.squeeze(x, dim=0)
        else:
            input = x
        if self.backbone == "resnet18":
            x1 = self.axial_net(input)
        elif self.backbone == "alexnet":
            x1 = self.axial_net.features(input)
        elif self.backbone == "vgg16":
            x1 = self.net(input)

        x2 = self.gap(x1).view(x1.size(0), -1)

        x3 = torch.max(x2, 0, keepdim=True)[0]

        out = self.classifier(x3)

        return out
