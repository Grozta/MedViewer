import torch
import torch.nn as nn
from torch.nn import functional as F
import numpy as np
from batchgenerators.augmentations.utils import pad_nd_image
from tqdm import tqdm


from torch import nn
import torch

from .sync_batchnormal import SynchronizedBatchNorm3d




class PixelShuffle3D(nn.Module):
    # partial borrowed from https://github.com/assassint2017/PixelShuffle3D/blob/master/PixelShuffle3D.py

    def __init__(self, scale_factor, is_reverse=False):
        """
        :param scale_factor(int,list,tuple): Scale up/down factor, if the input scale_factor is int,
         x,y,z axes of a data will scale up/down with the same scale factor,
         else x,y,z axes of a data will scale with different scale factor
        :param is_reverse(bool): True for HDC, False for DUC.
        """
        if isinstance(scale_factor, int):
            self.scale_factor_x = self.scale_factor_y = self.scale_factor_z = scale_factor
        elif isinstance(scale_factor, tuple) or isinstance(scale_factor, list):
            self.scale_factor_x = scale_factor[0]
            self.scale_factor_y = scale_factor[1]
            self.scale_factor_z = scale_factor[2]
        else:
            print("scale factor should be int or tuple or list")
            raise ValueError
        super(PixelShuffle3D, self).__init__()
        self.is_reverse = is_reverse

    def forward(self, inputs):
        batch_size, channels, in_depth, in_height, in_width = inputs.size()
        if self.is_reverse:  # for HDC
            out_channels = channels * self.scale_factor_x * self.scale_factor_y * self.scale_factor_z
            out_depth  = in_depth  // self.scale_factor_x
            out_height = in_height // self.scale_factor_y
            out_width  = in_width  // self.scale_factor_z
            input_view = inputs.contiguous().view(
                batch_size, channels,
                out_depth , self.scale_factor_x,
                out_height, self.scale_factor_y,
                out_width , self.scale_factor_z)
            shuffle_out = input_view.permute(0, 1, 3, 5, 7, 2, 4, 6).contiguous()
            return shuffle_out.view(batch_size, out_channels, out_depth, out_height, out_width)
        else:  # for DUC
            channels //= (
                        self.scale_factor_x * self.scale_factor_y * self.scale_factor_z)
            # out channels, it should equal to class number for segmentation task

            out_depth  = in_depth  * self.scale_factor_x
            out_height = in_height * self.scale_factor_y
            out_width  = in_width  * self.scale_factor_z
            # nn.PixelShuffle
            input_view = inputs.contiguous().view(
                batch_size, channels,
                self.scale_factor_x, self.scale_factor_y, self.scale_factor_z,
                in_depth,            in_height,           in_width)

            shuffle_out = input_view.permute(0, 1, 5, 2, 6, 3, 7, 4).contiguous()
            return shuffle_out.view(batch_size, channels, out_depth, out_height, out_width)


class DUC(nn.Module):

    def __init__(self, upscale_factor, class_num, in_channels):
        """
        reference paper: Shi, W., Caballero, J., Huszár, F., Totz, J., Aitken, A. P., Bishop, R., ... & Wang, Z. (2016).
         Real-time single image and video super-resolution using an efficient sub-pixel convolutional neural network.
          In Proceedings of the IEEE conference on computer vision and pattern recognition (pp. 1874-1883).
        3D DUC module, the input data dimensions should be 5D tensor like(batch, channel, x, y, z),
        workflow: conv->batchnorm->relu->pixelshuffle
        :param upscale_factor(int, tuple, list): Scale up factor, if the input scale_factor is int,
         x,y,z axes of a data will scale up with the same scale factor,
         else x,y,z axes of a data will scale with different scale factor
        :param class_num(int): the number of total classes (background and instance)
        :param in_channels(int): the number of input channel
        """
        super(DUC, self).__init__()
        if isinstance(upscale_factor, int):
            scale_factor_x = scale_factor_y = scale_factor_z = upscale_factor
        elif isinstance(upscale_factor, tuple) or isinstance(upscale_factor, list):
            scale_factor_x = upscale_factor[0]
            scale_factor_y = upscale_factor[1]
            scale_factor_z = upscale_factor[2]
        else:
            print("scale factor should be int or tuple")
            raise ValueError
        # self.conv = nn.Conv3d(in_channels, class_num * scale_factor_x * scale_factor_y * scale_factor_z, kernel_size=3, padding=1)
        self.activation = nn.ReLU(inplace=False)
        self.conv = HDC_module(in_channels, class_num * scale_factor_x * scale_factor_y * scale_factor_z, self.activation)
        # self.bn = nn.BatchNorm3d(class_num * scale_factor_x * scale_factor_y * scale_factor_z)
        # self.relu = nn.ReLU(inplace=True)
        self.ps = PixelShuffle3D(upscale_factor, is_reverse=False)

    def forward(self, x):
        x = self.conv(x)
        # x = self.bn(x)
        # x = self.relu(x)
        x = self.ps(x)
        return x

class Conv_1x1x1(nn.Module):
    def __init__(self, in_dim, out_dim, activation):
        super(Conv_1x1x1, self).__init__()
        self.conv1 = nn.Conv3d(in_dim, out_dim, kernel_size=1, stride=1, padding=0, bias=True)
        self.norm = SynchronizedBatchNorm3d(out_dim)
        self.act = activation

    def forward(self, x):
        x = self.act(self.norm(self.conv1(x)))
        return x


class Conv_3x3x1(nn.Module):
    def __init__(self, in_dim, out_dim, activation):
        super(Conv_3x3x1, self).__init__()
        self.conv1 = nn.Conv3d(in_dim, out_dim, kernel_size=(3, 3, 1), stride=1, padding=(1, 1, 0), bias=True)
        self.norm = SynchronizedBatchNorm3d(out_dim)
        self.act = activation

    def forward(self, x):
        x = self.act(self.norm(self.conv1(x)))
        return x


class Conv_1x3x3(nn.Module):
    def __init__(self, in_dim, out_dim, activation):
        super(Conv_1x3x3, self).__init__()
        self.conv1 = nn.Conv3d(in_dim, out_dim, kernel_size=(1, 3, 3), stride=1, padding=(0, 1, 1), bias=True)
        self.norm = SynchronizedBatchNorm3d(out_dim)
        self.act = activation

    def forward(self, x):
        x = self.act(self.norm(self.conv1(x)))
        return x


class Conv_3x3x3(nn.Module):
    def __init__(self, in_dim, out_dim, activation):
        super(Conv_3x3x3, self).__init__()
        self.conv1 = nn.Conv3d(in_dim, out_dim, kernel_size=(3, 3, 3), stride=1, padding=(1, 1, 1), bias=True)
        self.norm = SynchronizedBatchNorm3d(out_dim)
        self.act = activation

    def forward(self, x):
        x = self.act(self.norm(self.conv1(x)))
        return x


class Conv_down(nn.Module):
    def __init__(self, in_dim, out_dim, activation):
        super(Conv_down, self).__init__()
        self.conv1 = nn.Conv3d(in_dim, out_dim, kernel_size=(3, 3, 3), stride=2, padding=(1, 1, 1), bias=True)
        self.norm = SynchronizedBatchNorm3d(out_dim)
        self.act = activation

    def forward(self, x):
        x = self.act(self.norm(self.conv1(x)))
        return x


class HDC_module(nn.Module):
    def __init__(self, in_dim, out_dim, activation):
        super(HDC_module, self).__init__()
        self.in_dim = in_dim
        self.out_dim = out_dim
        self.inter_dim = in_dim // 4
        self.out_inter_dim = out_dim // 4
        self.conv_3x3x1_1 = Conv_3x3x1(self.out_inter_dim, self.out_inter_dim, activation)
        self.conv_3x3x1_2 = Conv_3x3x1(self.out_inter_dim, self.out_inter_dim, activation)
        self.conv_3x3x1_3 = Conv_3x3x1(self.out_inter_dim, self.out_inter_dim, activation)
        self.conv_3x3x1_4 = Conv_3x3x1(self.out_inter_dim, self.out_inter_dim, activation)
        self.conv_1x1x1_1 = Conv_1x1x1(in_dim, out_dim, activation)
        self.conv_1x1x1_2 = Conv_1x1x1(out_dim, out_dim, activation)
        if self.in_dim > self.out_dim:
            self.conv_1x1x1_3 = Conv_1x1x1(in_dim, out_dim, activation)
        self.conv_1x3x3 = Conv_1x3x3(out_dim, out_dim, activation)

    def forward(self, x):
        x_1 = self.conv_1x1x1_1(x)
        x1 = x_1[:, 0:self.out_inter_dim, ...]
        x2 = x_1[:, self.out_inter_dim:self.out_inter_dim * 2, ...]
        x3 = x_1[:, self.out_inter_dim * 2:self.out_inter_dim * 3, ...]
        x4 = x_1[:, self.out_inter_dim * 3:self.out_inter_dim * 4, ...]
        x2 = self.conv_3x3x1_1(x2)
        x3 = self.conv_3x3x1_2(x2 + x3)
        x4 = self.conv_3x3x1_3(x3 + x4)

        x_1 = torch.cat((x1, x2, x3, x4), dim=1)
        x_1 = self.conv_1x1x1_2(x_1)
        if self.in_dim > self.out_dim:
            x = self.conv_1x1x1_3(x)
        x_1 = self.conv_1x3x3(x + x_1)
        return x_1


def conv_trans_block_3d(in_dim, out_dim, activation):
    return nn.Sequential(
        nn.ConvTranspose3d(in_dim, out_dim, kernel_size=3, stride=2, padding=1, output_padding=1),
        SynchronizedBatchNorm3d(out_dim),
        activation)


device1 = torch.device("cuda")


def hdc(image, num=2):
    x1 = torch.Tensor([]).to(device1)
    for i in range(num):
        for j in range(num):
            for k in range(num):
                x3 = image[:, :, k::num, i::num, j::num]
                x1 = torch.cat((x1, x3), dim=1)
    return x1


class HDC_Net(nn.Module):
    def __init__(self, in_dim, out_dim, num_filters=8):
        super(HDC_Net, self).__init__()

        self.conv_op = None
        self.num_classes = 2
        self.inference_apply_nonlin = lambda x: x
        self.input_channels_pbl = None
        self._gaussian_3d = None

        self.in_dim = in_dim
        self.out_dim = out_dim
        self.n_f = num_filters
        self.activation = nn.ReLU(inplace=False)
        # down
        self.conv_3x3x3 = Conv_3x3x3(8, self.n_f, self.activation)
        self.conv_1 = HDC_module(self.n_f, self.n_f, self.activation)
        self.down_1 = Conv_down(self.n_f, self.n_f, self.activation)
        self.conv_2 = HDC_module(self.n_f, self.n_f, self.activation)
        self.down_2 = Conv_down(self.n_f, self.n_f, self.activation)
        self.conv_3 = HDC_module(self.n_f, self.n_f, self.activation)
        self.down_3 = Conv_down(self.n_f, self.n_f, self.activation)
        # bridge
        self.bridge = HDC_module(self.n_f, self.n_f, self.activation)
        # up
        self.up_1 = conv_trans_block_3d(self.n_f, self.n_f, self.activation)
        self.conv_4 = HDC_module(self.n_f * 2, self.n_f, self.activation)
        self.up_2 = conv_trans_block_3d(self.n_f, self.n_f, self.activation)
        self.conv_5 = HDC_module(self.n_f * 2, self.n_f, self.activation)
        self.up_3 = conv_trans_block_3d(self.n_f, self.n_f, self.activation)
        self.conv_6 = HDC_module(self.n_f * 2, self.n_f, self.activation)

        self.duc = DUC(2,2,self.n_f)

        # self.upsample = nn.Upsample(scale_factor=2, mode='trilinear', align_corners=False)
        # self.upsample = conv_trans_block_3d(self.n_f, self.n_f, self.activation)
        # self.out = nn.Conv3d(self.n_f, out_dim, kernel_size=1, stride=1, padding=0)
        self.softmax = nn.Softmax(dim=1)
        for m in self.modules():
            if isinstance(m, nn.Conv3d):
                torch.nn.init.torch.nn.init.kaiming_normal_(m.weight)  #
            elif isinstance(m, nn.BatchNorm3d) or isinstance(m, nn.GroupNorm) or isinstance(m, SynchronizedBatchNorm3d):
                nn.init.constant_(m.weight, 1)
                nn.init.constant_(m.bias, 0)



    def forward(self, x):

        x = hdc(x)
        x = self.conv_3x3x3(x)
        x1 = self.conv_1(x)
        x = self.down_1(x1)
        x2 = self.conv_2(x)
        x = self.down_2(x2)
        x3 = self.conv_3(x)
        x = self.down_3(x3)
        x = self.bridge(x)
        x = self.up_1(x)
        x = torch.cat((x, x3), dim=1)
        x = self.conv_4(x)
        x = self.up_2(x)
        x = torch.cat((x, x2), dim=1)
        x = self.conv_5(x)
        x = self.up_3(x)
        x = torch.cat((x, x1), dim=1)
        x = self.conv_6(x)
        x = self.duc(x)
        # x = self.upsample(x)
        # x = self.out(x)
        # x = self.softmax(x)
        return x

# from fvcore.nn import parameter_count_table

if __name__ == "__main__":
    # from thop import profile
    # device = torch.device('cuda')
    # image_size = 128
    # x = torch.rand((1, 4, 128, 128, 128), device=device)
    # print("x size: {}".format(x.size()))
    # model = HDC_Net(in_dim=4, out_dim=4, num_filters=32).to(device)
    # # flops, params = profile(model, inputs=(x,))
    # # print("***********")
    # # print(flops, params)
    # # print("***********")
    # out = model(x)
    # print("out size: {}".format(out.size()))
    model = HDC_Net(1,2,32)
    # print(parameter_count_table(model))