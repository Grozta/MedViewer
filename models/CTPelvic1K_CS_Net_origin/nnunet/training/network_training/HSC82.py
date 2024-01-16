# full assembly of the sub-parts to form the complete net
import torch
import torch.nn as nn
import numpy as np
from batchgenerators.augmentations.utils import pad_nd_image
from tqdm import tqdm

from models.CTPelvic1K_CS_Net_origin.nnunet.utilities.tensor_utilities import flip
from models.CTPelvic1K_CS_Net_origin.nnunet.utilities.to_torch import to_cuda, maybe_to_torch
from torch import nn
import torch
from scipy.ndimage.filters import gaussian_filter


class Conv_block(nn.Module):
    def __init__(self, in_ch, out_ch, size):
        super(Conv_block, self).__init__()
        self.padding = [(size[0] - 1) // 2, (size[1] - 1) // 2]
        self.conv = nn.Conv2d(in_ch, out_ch, size, padding=self.padding, stride=1)
        self.norm = nn.InstanceNorm2d(out_ch)
        self.act = nn.ReLU(inplace=True)

    def forward(self, x):
        return self.act(self.norm(self.conv(x)))


class Double_conv(nn.Module):
    def __init__(self, in_ch, out_ch):
        super(Double_conv, self).__init__()
        self.branchs = 6
        self.in_ch = in_ch
        self.mid_mid = out_ch // self.branchs
        self.out_ch = out_ch
        self.conv1x1_mid = Conv_block(self.in_ch, self.out_ch, [1, 1])
        self.conv1x1_2 = nn.Conv2d(self.out_ch, self.out_ch, 1)
        self.conv3x3_2_1 = Conv_block(self.mid_mid, self.mid_mid, [1, 3])
        self.conv3x3_1_1 = Conv_block(self.mid_mid, self.mid_mid, [1, 3])
        self.conv3x3_1 = Conv_block(self.mid_mid, self.mid_mid, [1, 3])
        self.conv3x1_1 = Conv_block(self.mid_mid, self.mid_mid, [1, 3])
        self.conv1x3_1 = Conv_block(self.mid_mid, self.mid_mid, [1, 3])
        self.conv3x3_1_2 = Conv_block(self.mid_mid, self.mid_mid, [3, 1])
        self.conv3x3_2_2 = Conv_block(self.mid_mid, self.mid_mid, [3, 1])
        self.conv3x3_2 = Conv_block(self.mid_mid, self.mid_mid, [3, 1])
        self.conv3x1_2 = Conv_block(self.mid_mid, self.mid_mid, [3, 1])
        self.conv1x3_2 = Conv_block(self.mid_mid, self.mid_mid, [3, 1])
        # self.conv1x1_2 = Conv_block(self.mid_mid, self.mid_mid, [1, 1])
        self.conv1x1_1 = nn.Conv2d(self.out_ch, self.out_ch, 1)
        # self.avg_pool = nn.AdaptiveAvgPool2d(1)
        self.num = max(self.mid_mid // 2, 12)
        # self.fc = nn.Linear(in_features=self.mid_mid, out_features=self.num)
        # self.fcs = nn.ModuleList([])
        # for i in range(self.branchs):
        #     self.fcs.append(nn.Linear(in_features=self.num, out_features=self.mid_mid))
        # self.softmax = nn.Softmax(dim=1)

        self.rel = nn.ReLU(inplace=True)
        if self.in_ch > self.out_ch:
            self.short_connect = nn.Conv2d(in_ch, out_ch, 1, padding=0)

    def forward(self, x):
        short = x
        if self.in_ch > self.out_ch:
            short = self.short_connect(x)
        xxx = self.conv1x1_mid(x)
        x0 = xxx[:, 0:self.mid_mid, ...]
        x1 = xxx[:, self.mid_mid:self.mid_mid * 2, ...]
        x2 = xxx[:, self.mid_mid * 2:self.mid_mid * 3, ...]
        x3 = xxx[:, self.mid_mid * 3:self.mid_mid * 4, ...]
        x4 = xxx[:, self.mid_mid * 4:self.mid_mid * 5, ...]
        x5 = xxx[:, self.mid_mid * 5:self.mid_mid * 6, ...]
        x1 = self.conv1x3_1(x1 + x0)
        x2 = self.conv3x1_1(x2 + x1)
        x3 = self.conv3x3_1(x3 + x2)
        x4 = self.conv3x3_1_1(x4 + x3)
        x5 = self.conv3x3_2_1(x5 + x4)
        # xx = x0 + x1 + x2 + x3 + x4 + x5
        # sk1 = self.avg_pool(xx)
        # sk1 = sk1.view(sk1.size(0), -1)
        # print(sk1.shape)
        # sk2 = self.fc(sk1)
        # for i, fc in enumerate(self.fcs):
        #     vector = fc(sk2).unsqueeze(1)
        #     if i == 0:
        #         attention_vector = vector
        #     else:
        #         attention_vector = torch.cat([attention_vector, vector], dim=1)
        # attention_vector = self.softmax(attention_vector)
        # attention_vector = attention_vector.unsqueeze(-1).unsqueeze(-1)
        # print(attention_vector[:,0,...].shape)
        # x0 = x0 * attention_vector[:, 0, ...]
        # x1 = x1 * attention_vector[:, 1, ...]
        # x2 = x2 * attention_vector[:, 2, ...]
        # x3 = x3 * attention_vector[:, 3, ...]
        # x4 = x4 * attention_vector[:, 4, ...]
        # x5 = x5 * attention_vector[:, 5, ...]
        xx = torch.cat((x0, x1, x2, x3, x4, x5), dim=1)
        xxx = self.conv1x1_1(xx)
        x0 = xxx[:, 0:self.mid_mid, ...]
        x1_2 = xxx[:, self.mid_mid:self.mid_mid * 2, ...]
        x2_2 = xxx[:, self.mid_mid * 2:self.mid_mid * 3, ...]
        x3_2 = xxx[:, self.mid_mid * 3:self.mid_mid * 4, ...]
        x4_2 = xxx[:, self.mid_mid * 4:self.mid_mid * 5, ...]
        x5_2 = xxx[:, self.mid_mid * 5:self.mid_mid * 6, ...]
        x1 = self.conv1x3_2(x1_2 + x0)  # !!!!!!
        x2 = self.conv3x1_2(x1 + x2_2)
        x3 = self.conv3x3_2(x2 + x3_2)
        x4 = self.conv3x3_1_2(x3 + x4_2)
        x5 = self.conv3x3_2_2(x4 + x5_2)
        xx = torch.cat((x0, x1, x2, x3, x4, x5), dim=1)
        xxx = self.conv1x1_2(xx)
        return self.rel(xxx + short)


# class Double_conv(nn.Module):
#     def __init__(self, in_ch, out_ch):
#         super(Double_conv, self).__init__()
#         self.branchs = 6
#         self.in_ch = in_ch
#         self.mid_mid = out_ch // self.branchs
#         self.out_ch = out_ch
#         self.conv1x1_mid = Conv_block(self.in_ch, self.out_ch, [1, 1])
#         self.conv1x1_2 = nn.Conv2d(self.out_ch, self.out_ch, 1)
#         self.conv3x3_2_1 = Conv_block(self.mid_mid, self.mid_mid, [1, 3])
#         self.conv3x3_1_1 = Conv_block(self.mid_mid, self.mid_mid, [1, 3])
#         self.conv3x3_1 = Conv_block(self.mid_mid, self.mid_mid, [1, 3])
#         self.conv3x1_1 = Conv_block(self.mid_mid, self.mid_mid, [1, 3])
#         self.conv1x3_1 = Conv_block(self.mid_mid, self.mid_mid, [1, 3])
#         self.conv3x3_1_2 = Conv_block(self.mid_mid, self.mid_mid, [3, 1])
#         self.conv3x3_2_2 = Conv_block(self.mid_mid, self.mid_mid, [3, 1])
#         self.conv3x3_2 = Conv_block(self.mid_mid, self.mid_mid, [3, 1])
#         self.conv3x1_2 = Conv_block(self.mid_mid, self.mid_mid, [3, 1])
#         self.conv1x3_2 = Conv_block(self.mid_mid, self.mid_mid, [3, 1])
#         self.conv1x1_2 = Conv_block(self.mid_mid, self.mid_mid, [1, 1])
#         self.conv1x1_1 = nn.Conv2d(self.out_ch, self.out_ch, 1)
#         self.avg_pool = nn.AdaptiveAvgPool2d(1)
#         self.num = max(self.mid_mid // 2, 12)
#         self.fc = nn.Linear(in_features=self.mid_mid, out_features=self.num)
#         self.fcs = nn.ModuleList([])
#         for i in range(self.branchs):
#             self.fcs.append(nn.Linear(in_features=self.num, out_features=self.mid_mid))
#         self.softmax = nn.Softmax(dim=1)
#
#         self.rel = nn.ReLU(inplace=True)
#         if self.in_ch > self.out_ch:
#             self.short_connect = nn.Conv2d(in_ch, out_ch, 1, padding=0)
#
#     def forward(self, x):
#         short = x
#         if self.in_ch > self.out_ch:
#             short = self.short_connect(x)
#         xxx = self.conv1x1_mid(x)
#         x0 = xxx[:, 0:self.mid_mid, ...]
#         x1 = xxx[:, self.mid_mid:self.mid_mid * 2, ...]
#         x2 = xxx[:, self.mid_mid * 2:self.mid_mid * 3, ...]
#         x3 = xxx[:, self.mid_mid * 3:self.mid_mid * 4, ...]
#         x4 = xxx[:, self.mid_mid * 4:self.mid_mid * 5, ...]
#         x5 = xxx[:, self.mid_mid * 5:self.mid_mid * 6, ...]
#         x1 = self.conv1x3_1(x1 + x0)
#         x2 = self.conv3x1_1(x2 + x1)
#         x3 = self.conv3x3_1(x3 + x2)
#         x4 = self.conv3x3_1_1(x4 + x3)
#         x5 = self.conv3x3_2_1(x5 + x4)
#         xx = x0 + x1 + x2 + x3 + x4 + x5
#         sk1 = self.avg_pool(xx)
#         sk1 = sk1.view(sk1.size(0), -1)
#         # print(sk1.shape)
#         sk2 = self.fc(sk1)
#         for i, fc in enumerate(self.fcs):
#             vector = fc(sk2).unsqueeze(1)
#             if i == 0:
#                 attention_vector = vector
#             else:
#                 attention_vector = torch.cat([attention_vector, vector], dim=1)
#         attention_vector = self.softmax(attention_vector)
#         attention_vector = attention_vector.unsqueeze(-1).unsqueeze(-1)
#         # print(attention_vector[:,0,...].shape)
#         x0 = x0 * attention_vector[:, 0, ...]
#         x1 = x1 * attention_vector[:, 1, ...]
#         x2 = x2 * attention_vector[:, 2, ...]
#         x3 = x3 * attention_vector[:, 3, ...]
#         x4 = x4 * attention_vector[:, 4, ...]
#         x5 = x5 * attention_vector[:, 5, ...]
#         xx = torch.cat((x0, x1, x2, x3, x4, x5), dim=1)
#         xxx = self.conv1x1_1(xx)
#         x0 = xxx[:, 0:self.mid_mid, ...]
#         x1_2 = xxx[:, self.mid_mid:self.mid_mid * 2, ...]
#         x2_2 = xxx[:, self.mid_mid * 2:self.mid_mid * 3, ...]
#         x3_2 = xxx[:, self.mid_mid * 3:self.mid_mid * 4, ...]
#         x4_2 = xxx[:, self.mid_mid * 4:self.mid_mid * 5, ...]
#         x5_2 = xxx[:, self.mid_mid * 5:self.mid_mid * 6, ...]
#         x1 = self.conv1x3_2(x1_2 + x0)  # !!!!!!
#         x2 = self.conv3x1_2(x1 + x2_2)
#         x3 = self.conv3x3_2(x2 + x3_2)
#         x4 = self.conv3x3_1_2(x3 + x4_2)
#         x5 = self.conv3x3_2_2(x4 + x5_2)
#         xx = torch.cat((x0, x1, x2, x3, x4, x5), dim=1)
#         xxx = self.conv1x1_2(xx)
#         return self.rel(xxx + short)


class Conv_down_2(nn.Module):
    def __init__(self, in_ch, out_ch):
        super(Conv_down_2, self).__init__()
        self.conv = nn.Conv2d(in_ch, in_ch, kernel_size=3, padding=1, stride=2, bias=True)
        self.norm = nn.InstanceNorm2d(out_ch)
        self.act = nn.ReLU(inplace=True)
        # self.pool = nn.MaxPool2d(kernel_size=2, stride=2)

    def forward(self, x):
        return self.act(self.norm(self.conv(x)))


class Conv_down(nn.Module):
    '''(conv => ReLU) * 2 => MaxPool2d'''

    def __init__(self, in_ch, out_ch, flage):
        """
        Args:
            in_ch(int) : input channel
            out_ch(int) : output channel
        """
        super(Conv_down, self).__init__()
        self.in_ch = in_ch
        self.out_ch = out_ch
        self.flage = flage
        if self.in_ch == 1:
            self.first = nn.Sequential(
                Conv_block(self.in_ch, self.out_ch, [3, 3]),
                Double_conv(self.out_ch, self.out_ch),
            )
            self.pool = nn.MaxPool2d(kernel_size=2, stride=2)
            self.conv_down = Conv_down_2(self.out_ch, self.out_ch)
        else:
            self.conv = Double_conv(self.in_ch, self.out_ch)
            self.pool = nn.MaxPool2d(kernel_size=2, stride=2)
            self.conv_down = Conv_down_2(self.in_ch, self.out_ch)

    def forward(self, x):
        if self.in_ch == 1:
            x = self.first(x)
            pool_x = torch.cat((self.pool(x), self.conv_down(x)), dim=1)
        else:
            x = self.conv(x)
            if self.flage == True:
                pool_x = torch.cat((self.pool(x), self.conv_down(x)), dim=1)
            else:
                pool_x = None
        return pool_x, x


class side_output(nn.Module):
    def __init__(self, inChans, outChans, factor, padding):
        super(side_output, self).__init__()
        self.conv0 = nn.Conv2d(inChans, outChans, 3, 1, 1)
        self.transconv1 = nn.ConvTranspose2d(outChans, outChans, 2 * factor, factor, padding=padding)

    def forward(self, x):
        out = self.conv0(x)
        out = self.transconv1(out)
        return out


def hdc(image, device, num=2):
    x1 = torch.Tensor([]).to(image.device)
    for i in range(num):
        for j in range(num):
            x3 = image[:, :, i::num, j::num]
            x1 = torch.cat((x1, x3), dim=1)
    return x1


class Conv_up(nn.Module):
    def __init__(self, in_ch, out_ch):
        super(Conv_up, self).__init__()
        self.up = nn.Conv2d(in_ch, out_ch, kernel_size=1, padding=0, stride=1)
        self.conv = Double_conv(in_ch, out_ch)
        self.interp = nn.Upsample(scale_factor=2, mode='bilinear', align_corners=False)

    def forward(self, x1, x2):
        x1 = self.interp(x1)
        x1 = self.up(x1)
        x1 = torch.cat((x1, x2), dim=1)
        x1 = self.conv(x1)
        return x1


class PGS_Net(nn.Module):
    def __init__(self, in_channels, out_channels, device, has_dropout=False):
        super(PGS_Net, self).__init__()
        self.input_shape_must_be_divisible_by = None
        self.conv_op = None
        self.num_classes = None
        self.inference_apply_nonlin = lambda x: x

        self.has_dropout = has_dropout
        self.in_channels = in_channels
        self.out_channels = out_channels

        self.device = device
        self.filter_channel = 36
        self.first = Conv_block(in_channels * 4, self.filter_channel, [3, 3])

        self.Conv_down1 = Conv_down(self.filter_channel, self.filter_channel, True)
        self.Conv_down2 = Conv_down(self.filter_channel * 2, self.filter_channel * 2, True)
        self.Conv_down3 = Conv_down(self.filter_channel * 4, self.filter_channel * 4, True)
        # self.Conv_down4 = Conv_down(512, 512,True)
        self.Conv_down5 = Conv_down(self.filter_channel * 8, self.filter_channel * 8, False)

        # self.Conv_up1 = Conv_up(1024,280)
        self.Conv_up2 = Conv_up(self.filter_channel * 8, self.filter_channel * 4)
        self.Conv_up3 = Conv_up(self.filter_channel * 4, self.filter_channel * 2)
        self.Conv_up4 = Conv_up(self.filter_channel * 2, self.filter_channel)

        self.Conv_up5 = Double_conv(self.filter_channel, self.filter_channel)
        # self.Conv_up6 = Double_conv(72, 72)
        # self.Conv_up7 = Double_conv(72, 72)

        self.up = nn.Upsample(scale_factor=2, mode='bilinear', align_corners=False)
        self.Conv_out = nn.Conv2d(self.filter_channel, out_channels, 1, padding=0, stride=1)

        # self.up_c = nn.Upsample(scale_factor=2, mode='bilinear', align_corners=False)
        # self.Conv_out_c = nn.Conv2d(72, 1, 1, padding=0, stride=1)

    def get_device(self):
        if next(self.parameters()).device == "cpu":
            return "cpu"
        else:
            return next(self.parameters()).device.index

    def set_device(self, device):
        if device == "cpu":
            self.cpu()
        else:
            self.cuda(device)

    def predict_3D(self, x, do_mirroring: bool, num_repeats=1, use_train_mode=False, batch_size=1,
                   mirror_axes=(0, 1, 2),
                   tiled=False, tile_in_z=True, step=2, patch_size=None, regions_class_order=None, use_gaussian=False,
                   pad_border_mode="edge", pad_kwargs=None, all_in_gpu=False):
        """
        :param x: (c, x, y , z)
        :param do_mirroring: whether or not to do test time data augmentation by mirroring
        :param num_repeats: how often should each patch be predicted? This MUST be 1 unless you are using monte carlo
        dropout sampling (for which you also must set use_train_mode=True)

        :param use_train_mode: sets the model to train mode. This functionality is kinda broken because it should not
        set batch norm to train mode! Do not use!
        :param batch_size: also used for monte carlo sampling, leave it at 1
        :param mirror_axes: the spatial axes along which the mirroring takes place, if applicable

        :param tiled: if False then prediction is fully convolutional (careful with large images!). Else we use sliding window
        :param tile_in_z: what a bad name. If x is (c, x, y, z), then this sets whether we do for sliding window the
        axis x or whether we do that one fully convolutionally. I suggest you don't use this (set tile_in_z=True)
        :param step: how large is the step size for sliding window? 2 = patch_size // 2 for each axis
        :param patch_size: if tiled prediction, how large are the patches that we use?
        :param regions_class_order: Don't use this. Fabian only.
        :param use_gaussian: set this to True to prevent stitching artifacts
        :param all_in_gpu: only affects _internal_predict_3D_3Dconv_tiled, _internal_predict_3D_2Dconv_tiled, _internal_predict_3D_2Dconv,
        _internal_predict_2D_2Dconv_tiled
        :return:
        """
        print("debug: mirroring: ", do_mirroring, "; mirror_axes: ", mirror_axes)
        assert self.get_device() != "cpu", "CPU not implemented"

        if len(mirror_axes) > 0 and max(mirror_axes) > 2:
            raise ValueError("mirror axes. duh")

        current_mode = self.training
        if use_train_mode is not None and use_train_mode:
            raise RuntimeError(
                "use_train_mode=True is currently broken! @Fabian needs to fix this (don't put batchnorm layer into train, just dropout)")
            self.train()
        elif use_train_mode is not None and not use_train_mode:
            self.eval()
        else:
            pass

        assert len(x.shape) == 4, "data must have shape (c,x,y,z)"

        if self.conv_op == nn.Conv3d:
            if tiled:
                res = self._internal_predict_3D_3Dconv_tiled(x, num_repeats, batch_size, tile_in_z, step, do_mirroring,
                                                             mirror_axes, patch_size, regions_class_order, use_gaussian,
                                                             pad_border_mode, pad_kwargs=pad_kwargs,
                                                             all_in_gpu=all_in_gpu)
            else:
                res = self._internal_predict_3D_3Dconv(x, do_mirroring, num_repeats, patch_size, batch_size,
                                                       mirror_axes, regions_class_order, pad_border_mode,
                                                       pad_kwargs=pad_kwargs)
        elif self.conv_op == nn.Conv2d:
            if tiled:
                res = self._internal_predict_3D_2Dconv_tiled(x, do_mirroring, num_repeats, batch_size, mirror_axes,
                                                             step, patch_size, regions_class_order, use_gaussian,
                                                             pad_border_mode, pad_kwargs=pad_kwargs,
                                                             all_in_gpu=all_in_gpu)
            else:
                res = self._internal_predict_3D_2Dconv(x, do_mirroring, num_repeats, patch_size, batch_size,
                                                       mirror_axes, regions_class_order, pad_border_mode,
                                                       pad_kwargs=pad_kwargs, all_in_gpu=all_in_gpu)
        else:
            raise RuntimeError("Invalid conv op, cannot determine what dimensionality (2d/3d) the network is")

        if use_train_mode is not None:
            self.train(current_mode)
        return res

    def predict_2D(self, x, do_mirroring, num_repeats=1, use_train_mode=False, batch_size=1, mirror_axes=(0, 1),
                   tiled=False, step=2, patch_size=None, regions_class_order=None, use_gaussian=False,
                   pad_border_mode="edge", pad_kwargs=None, all_in_gpu=False):

        assert self.get_device() != "cpu", "CPU not implemented"

        if len(mirror_axes) > 0 and max(mirror_axes) > 1:
            raise ValueError("mirror axes. duh")

        assert len(x.shape) == 3, "data must have shape (c,x,y)"

        current_mode = self.training
        if use_train_mode is not None and use_train_mode:
            self.train()
        elif use_train_mode is not None and not use_train_mode:
            self.eval()
        else:
            pass

        if self.conv_op == nn.Conv3d:
            raise RuntimeError("Cannot predict 2d if the network is 3d. Dummy.")
        elif self.conv_op == nn.Conv2d:
            if tiled:
                res = self._internal_predict_2D_2Dconv_tiled(x, num_repeats, batch_size, step, do_mirroring,
                                                             mirror_axes, patch_size, regions_class_order,
                                                             use_gaussian, pad_border_mode, pad_kwargs=pad_kwargs,
                                                             all_in_gpu=all_in_gpu)
            else:
                res = self._internal_predict_2D_2Dconv(x, do_mirroring, num_repeats, None, batch_size, mirror_axes,
                                                       regions_class_order, pad_border_mode, pad_kwargs=pad_kwargs)
        else:
            raise RuntimeError("Invalid conv op, cannot determine what dimensionality (2d/3d) the network is")

        if use_train_mode is not None:
            self.train(current_mode)
        return res

    def _internal_predict_3D_3Dconv_tiled(self, x, num_repeats, BATCH_SIZE=None, tile_in_z=True, step=2,
                                          do_mirroring=True, mirror_axes=(0, 1, 2), patch_size=None,
                                          regions_class_order=None, use_gaussian=False, pad_border_mode="edge",
                                          pad_kwargs=None, all_in_gpu=False):
        """
        x must be (c, x, y, z)
        :param x:
        :param num_repeats:
        :param BATCH_SIZE:
        :param tile_in_z:
        :param step:
        :param do_mirroring:
        :param mirror_axes:
        :param patch_size:
        :param regions_class_order:
        :param use_gaussian:
        :param pad_border_mode:
        :param pad_kwargs:
        :param all_in_gpu: if True then data and prediction will be held in GPU for inference. Faster, but uses more vram
        :return:
        """
        assert len(x.shape) == 4, "x must be (c, x, y, z)"
        assert self.get_device() != "cpu"

        torch.cuda.empty_cache()

        with torch.no_grad():
            assert patch_size is not None, "patch_size cannot be None for tiled prediction"

            data, slicer = pad_nd_image(x, patch_size, pad_border_mode, pad_kwargs, True, None)

            data = data[None]

            if BATCH_SIZE is not None:
                data = np.vstack([data] * BATCH_SIZE)  ### ??? same data ???

            input_size = [1, x.shape[0]] + list(patch_size)
            if not tile_in_z:
                input_size[2] = data.shape[2]
                patch_size[0] = data.shape[2]
            input_size = [int(i) for i in input_size]

            a = torch.zeros(input_size, dtype=torch.float).cuda(self.get_device(), non_blocking=True)
            # dummy run to see number of classes
            networkresults = self(a)
            if isinstance(networkresults, tuple):
                nb_of_classes = networkresults[0].size()[1]
            else:
                nb_of_classes = networkresults.size()[1]

            if use_gaussian:
                tmp = np.zeros(patch_size)
                center_coords = [i // 2 for i in patch_size]
                sigmas = [i // 8 for i in patch_size]
                tmp[tuple(center_coords)] = 1
                tmp_smooth = gaussian_filter(tmp, sigmas, 0, mode='constant', cval=0)
                tmp_smooth = tmp_smooth / tmp_smooth.max() * 1
                add = tmp_smooth + 1e-8
            else:
                add = np.ones(patch_size, dtype=np.float32)

            add = add.astype(np.float32)

            data_shape = data.shape
            center_coord_start = np.array([i // 2 for i in patch_size]).astype(int)
            center_coord_end = np.array(
                [data_shape[i + 2] - patch_size[i] // 2 for i in range(len(patch_size))]).astype(int)

            num_steps = np.ceil(
                [(center_coord_end[i] - center_coord_start[i]) / (patch_size[i] / step) for i in range(3)])
            step_size = np.array(
                [(center_coord_end[i] - center_coord_start[i]) / (num_steps[i] + 1e-8) for i in range(3)])
            step_size[step_size == 0] = 9999999
            xsteps = np.round(np.arange(center_coord_start[0], center_coord_end[0] + 1e-8, step_size[0])).astype(int)
            ysteps = np.round(np.arange(center_coord_start[1], center_coord_end[1] + 1e-8, step_size[1])).astype(int)
            zsteps = np.round(np.arange(center_coord_start[2], center_coord_end[2] + 1e-8, step_size[2])).astype(int)

            if all_in_gpu:
                # some of these can remain in half. We just need the reuslts for softmax so it won't hurt at all to reduce
                # precision. Inference is of course done in float
                result = torch.zeros([nb_of_classes] + list(data.shape[2:]), dtype=torch.half).cuda()  ### ???
                data = torch.from_numpy(data).cuda(self.get_device())
                result_numsamples = torch.zeros([nb_of_classes] + list(data.shape[2:]), dtype=torch.half).cuda()
                add = torch.from_numpy(add).cuda(self.get_device()).float()
                add_torch = add
            else:
                result = np.zeros([nb_of_classes] + list(data.shape[2:]), dtype=np.float32)
                result_numsamples = np.zeros([nb_of_classes] + list(data.shape[2:]), dtype=np.float32)
                add_torch = torch.from_numpy(add).cuda(self.get_device(), non_blocking=True)

            # data, result and add_torch and result_numsamples are now on GPU
            for x in xsteps:
                lb_x = x - patch_size[0] // 2
                ub_x = x + patch_size[0] // 2
                for y in ysteps:
                    lb_y = y - patch_size[1] // 2
                    ub_y = y + patch_size[1] // 2
                    for z in zsteps:
                        lb_z = z - patch_size[2] // 2
                        ub_z = z + patch_size[2] // 2

                        predicted_patch = \
                            self._internal_maybe_mirror_and_pred_3D(data[:, :, lb_x:ub_x, lb_y:ub_y, lb_z:ub_z],
                                                                    num_repeats, mirror_axes, do_mirroring, add_torch)[
                                0]
                        if all_in_gpu:
                            predicted_patch = predicted_patch.half()
                        else:
                            predicted_patch = predicted_patch.cpu().numpy()

                        result[:, lb_x:ub_x, lb_y:ub_y, lb_z:ub_z] += predicted_patch

                        if all_in_gpu:
                            result_numsamples[:, lb_x:ub_x, lb_y:ub_y, lb_z:ub_z] += add.half()
                        else:
                            result_numsamples[:, lb_x:ub_x, lb_y:ub_y, lb_z:ub_z] += add

            slicer = tuple(
                [slice(0, result.shape[i]) for i in range(len(result.shape) - (len(slicer) - 1))] + slicer[1:])
            result = result[slicer]
            result_numsamples = result_numsamples[slicer]

            softmax_pred = result / result_numsamples

            # patient_data = patient_data[:, :old_shape[0], :old_shape[1], :old_shape[2]]
            if regions_class_order is None:
                predicted_segmentation = softmax_pred.argmax(0)
            else:
                if all_in_gpu:
                    softmax_pred_here = softmax_pred.detach().cpu().numpy()
                else:
                    softmax_pred_here = softmax_pred
                predicted_segmentation_shp = softmax_pred_here[0].shape
                predicted_segmentation = np.zeros(predicted_segmentation_shp, dtype=np.float32)
                for i, c in enumerate(regions_class_order):
                    predicted_segmentation[softmax_pred_here[i] > 0.5] = c

            if all_in_gpu:
                predicted_segmentation = predicted_segmentation.detach().cpu().numpy()
                softmax_pred = softmax_pred.half().detach().cpu().numpy()
        return predicted_segmentation, None, softmax_pred, None

    def _internal_predict_3D_3Dconv(self, x, do_mirroring, num_repeats, min_size=None, BATCH_SIZE=None,
                                    mirror_axes=(0, 1, 2), regions_class_order=None, pad_border_mode="edge",
                                    pad_kwargs=None):
        with torch.no_grad():
            x, slicer = pad_nd_image(x, min_size, pad_border_mode, pad_kwargs, True,
                                     self.input_shape_must_be_divisible_by)
            # x, old_shape = pad_patient_3D_incl_c(x, self.input_shape_must_be_divisible_by, min_size)

            new_shp = x.shape

            data = np.zeros(tuple([1] + list(new_shp)), dtype=np.float32)

            data[0] = x

            if BATCH_SIZE is not None:
                data = np.vstack([data] * BATCH_SIZE)

            stacked = self._internal_maybe_mirror_and_pred_3D(data, num_repeats, mirror_axes, do_mirroring, None)[0]

            slicer = tuple(
                [slice(0, stacked.shape[i]) for i in range(len(stacked.shape) - (len(slicer) - 1))] + slicer[1:])
            stacked = stacked[slicer]
            softmax_pred = stacked

            if regions_class_order is None:
                predicted_segmentation = softmax_pred.argmax(0)
            else:
                predicted_segmentation_shp = softmax_pred[0].shape
                predicted_segmentation = np.zeros(predicted_segmentation_shp, dtype=np.float32)
                for i, c in enumerate(regions_class_order):
                    predicted_segmentation[softmax_pred[i] > 0.5] = c
        return predicted_segmentation, None, softmax_pred, None

    def _internal_predict_3D_2Dconv_tiled(self, data, do_mirroring, num_repeats, BATCH_SIZE=None, mirror_axes=(0, 1),
                                          step=2, patch_size=None, regions_class_order=None, use_gaussian=False,
                                          pad_border_mode="edge", pad_kwargs=None, all_in_gpu=False):
        if all_in_gpu:
            raise NotImplementedError
        assert len(data.shape) == 4, "data must be c, x, y, z"
        predicted_segmentation = []
        softmax_pred = []
        for s in tqdm(range(data.shape[1])):
            if self.input_channels_pbl > 1:
                mn = s - (self.input_channels_pbl - 1) // 2
                mx = s + (self.input_channels_pbl - 1) // 2 + 1
                valid_mn = max(mn, 0)
                valid_mx = min(mx, data.shape[1])
                data_input2D = data[:, valid_mn:valid_mx]
                need_to_pad_below = valid_mn - mn
                need_to_pad_above = mx - valid_mx

                if need_to_pad_below > 0:
                    shp_for_pad = np.array(data_input2D.shape)
                    shp_for_pad[1] = need_to_pad_below
                    data_input2D = np.concatenate((np.zeros(shp_for_pad), data_input2D), 1)
                if need_to_pad_above > 0:
                    shp_for_pad = np.array(data_input2D.shape)
                    shp_for_pad[1] = need_to_pad_above
                    data_input2D = np.concatenate((data_input2D, np.zeros(shp_for_pad)), 1)
                data_input2D = data_input2D.reshape((-1, data_input2D.shape[-2], data_input2D.shape[-1]))
                # print("data_input2D.shape: ", data_input2D.shape)  ### (7,605,605)
            else:
                data_input2D = data[:, s]
                # print("data_input2D.shape: ",data_input2D.shape)   ### (1,605,605)

            pred_seg, bayesian_predictions, softmax_pres, uncertainty = \
                self._internal_predict_2D_2Dconv_tiled(data_input2D, num_repeats, BATCH_SIZE, step, do_mirroring,
                                                       mirror_axes, patch_size, regions_class_order, use_gaussian,
                                                       pad_border_mode=pad_border_mode, pad_kwargs=pad_kwargs)
            predicted_segmentation.append(pred_seg[None])
            softmax_pred.append(softmax_pres[None])
        predicted_segmentation = np.vstack(predicted_segmentation)
        softmax_pred = np.vstack(softmax_pred).transpose((1, 0, 2, 3))
        return predicted_segmentation, None, softmax_pred, None

    def _internal_predict_3D_2Dconv(self, data, do_mirroring, num_repeats, min_size=None, BATCH_SIZE=None,
                                    mirror_axes=(0, 1), regions_class_order=None, pad_border_mode="edge",
                                    pad_kwargs=None,
                                    all_in_gpu=False):
        if all_in_gpu:
            raise NotImplementedError
        assert len(data.shape) == 4, "data must be c, x, y, z"
        predicted_segmentation = []
        softmax_pred = []
        for s in range(data.shape[1]):
            pred_seg, bayesian_predictions, softmax_pres, uncertainty = \
                self._internal_predict_2D_2Dconv(data[:, s], do_mirroring, num_repeats, min_size, BATCH_SIZE,
                                                 mirror_axes, regions_class_order, pad_border_mode, pad_kwargs)
            predicted_segmentation.append(pred_seg[None])
            softmax_pred.append(softmax_pres[None])
        predicted_segmentation = np.vstack(predicted_segmentation)
        softmax_pred = np.vstack(softmax_pred).transpose((1, 0, 2, 3))
        return predicted_segmentation, None, softmax_pred, None

    def _internal_predict_2D_2Dconv_tiled(self, patient_data, num_repeats, BATCH_SIZE=None, step=2,
                                          do_mirroring=True, mirror_axes=(0, 1), patch_size=None,
                                          regions_class_order=None,
                                          use_gaussian=False, pad_border_mode="edge", pad_kwargs=None,
                                          all_in_gpu=False):
        with torch.no_grad():
            tile_size = patch_size
            assert tile_size is not None, "patch_size cannot be None for tiled prediction"
            # pad images so that their size is a multiple of tile_size
            data, slicer = pad_nd_image(patient_data, tile_size, pad_border_mode, pad_kwargs, True)

            data = data[None]

            if BATCH_SIZE is not None:
                data = np.vstack([data] * BATCH_SIZE)

            input_size = [1, patient_data.shape[0]] + list(tile_size)
            input_size = [int(i) for i in input_size]
            a = torch.zeros(input_size, dtype=torch.float).cuda(self.get_device(), non_blocking=True)
            # print("data_shape in tailed: ",a.shape) #(1,7,512,512)

            # dummy run to see number of classes
            # nb_of_classes = self(a).size()[1]
            networkresults = self(a)
            if isinstance(networkresults, tuple):
                nb_of_classes = networkresults[0].size()[1]
            else:
                nb_of_classes = networkresults.size()[1]

            if use_gaussian:
                tmp = np.zeros(tile_size, dtype=np.float32)
                center_coords = [i // 2 for i in tile_size]
                sigmas = [i // 8 for i in tile_size]
                tmp[tuple(center_coords)] = 1
                tmp_smooth = gaussian_filter(tmp, sigmas, 0, mode='constant', cval=0)
                tmp_smooth = tmp_smooth / tmp_smooth.max() * 1
                add = tmp_smooth
            else:
                add = np.ones(tile_size, dtype=np.float32)

            add = add.astype(np.float32)

            data_shape = data.shape
            center_coord_start = np.array([i // 2 for i in patch_size]).astype(int)
            center_coord_end = np.array(
                [data_shape[i + 2] - patch_size[i] // 2 for i in range(len(patch_size))]).astype(int)
            num_steps = np.ceil(
                [(center_coord_end[i] - center_coord_start[i]) / (patch_size[i] / step) for i in range(2)])
            step_size = np.array(
                [(center_coord_end[i] - center_coord_start[i]) / (num_steps[i] + 1e-8) for i in range(2)])
            step_size[step_size == 0] = 9999999
            xsteps = np.round(np.arange(center_coord_start[0], center_coord_end[0] + 1e-8, step_size[0])).astype(int)
            ysteps = np.round(np.arange(center_coord_start[1], center_coord_end[1] + 1e-8, step_size[1])).astype(int)

            if all_in_gpu:
                # some of these can remain in half. We just need the reuslts for softmax so it won't hurt at all to reduce
                # precision. Inference is of course done in float
                result = torch.zeros([nb_of_classes] + list(data.shape[2:]), dtype=torch.half).cuda()
                data = torch.from_numpy(data).cuda(self.get_device())
                result_numsamples = torch.zeros([nb_of_classes] + list(data.shape[2:]), dtype=torch.half).cuda()
                add = torch.from_numpy(add).cuda(self.get_device()).float()
                add_torch = add
            else:
                result = np.zeros([nb_of_classes] + list(data.shape[2:]), dtype=np.float32)
                result_numsamples = np.zeros([nb_of_classes] + list(data.shape[2:]), dtype=np.float32)
                add_torch = torch.from_numpy(add).cuda(self.get_device(), non_blocking=True)

            for x in xsteps:
                lb_x = x - patch_size[0] // 2
                ub_x = x + patch_size[0] // 2
                for y in ysteps:
                    lb_y = y - patch_size[1] // 2
                    ub_y = y + patch_size[1] // 2
                    predicted_patch = \
                        self._internal_maybe_mirror_and_pred_2D(data[:, :, lb_x:ub_x, lb_y:ub_y],
                                                                num_repeats, mirror_axes, do_mirroring, add_torch)[0]
                    if all_in_gpu:
                        predicted_patch = predicted_patch.half()
                    else:
                        predicted_patch = predicted_patch.cpu().numpy()

                    result[:, lb_x:ub_x, lb_y:ub_y] += predicted_patch

                    if all_in_gpu:
                        result_numsamples[:, lb_x:ub_x, lb_y:ub_y] += add.half()
                    else:
                        result_numsamples[:, lb_x:ub_x, lb_y:ub_y] += add

            slicer = tuple(
                [slice(0, result.shape[i]) for i in range(len(result.shape) - (len(slicer) - 1))] + slicer[1:])
            result = result[slicer]
            result_numsamples = result_numsamples[slicer]

            softmax_pred = result / result_numsamples

            if regions_class_order is None:
                predicted_segmentation = softmax_pred.argmax(0)
            else:
                if all_in_gpu:
                    softmax_pred_here = softmax_pred.detach().cpu().numpy()
                else:
                    softmax_pred_here = softmax_pred
                predicted_segmentation_shp = softmax_pred_here[0].shape
                predicted_segmentation = np.zeros(predicted_segmentation_shp, dtype=np.float32)
                for i, c in enumerate(regions_class_order):
                    predicted_segmentation[softmax_pred_here[i] > 0.5] = c

            if all_in_gpu:
                predicted_segmentation = predicted_segmentation.detach().cpu().numpy()
                softmax_pred = softmax_pred.half().detach().cpu().numpy()
        return predicted_segmentation, None, softmax_pred, None

    def _internal_predict_2D_2Dconv(self, x, do_mirroring, num_repeats, min_size=None, BATCH_SIZE=None,
                                    mirror_axes=(0, 1), regions_class_order=None, pad_border_mode="edge",
                                    pad_kwargs=None):
        with torch.no_grad():
            _ = None
            # x, old_shape = pad_patient_2D_incl_c(x, self.input_shape_must_be_divisible_by, min_size)
            x, slicer = pad_nd_image(x, min_size, pad_border_mode, pad_kwargs, True,
                                     self.input_shape_must_be_divisible_by)
            """pad_res = []
            for i in range(x.shape[0]):
                t, old_shape = pad_patient_2D(x[i], self.input_shape_must_be_divisible_by, None)
                pad_res.append(t[None])

            x = np.vstack(pad_res)"""

            new_shp = x.shape

            data = np.zeros(tuple([1] + list(new_shp)), dtype=np.float32)

            data[0] = x

            if BATCH_SIZE is not None:
                data = np.vstack([data] * BATCH_SIZE)

            result = self._internal_maybe_mirror_and_pred_2D(data, num_repeats, mirror_axes, do_mirroring)[0]

            slicer = tuple(
                [slice(0, result.shape[i]) for i in range(len(result.shape) - (len(slicer) - 1))] + slicer[1:])
            result = result[slicer]
            softmax_pred = result

            if regions_class_order is None:
                predicted_segmentation = softmax_pred.argmax(0)
            else:
                predicted_segmentation_shp = softmax_pred[0].shape
                predicted_segmentation = np.zeros(predicted_segmentation_shp, dtype=np.float32)
                for i, c in enumerate(regions_class_order):
                    predicted_segmentation[softmax_pred[i] > 0.5] = c
        return predicted_segmentation, _, softmax_pred, _

    def _internal_maybe_mirror_and_pred_3D(self, x, num_repeats, mirror_axes, do_mirroring=True, mult=None):
        # everything in here takes place on the GPU. If x and mult are not yet on GPU this will be taken care of here
        # we now return a cuda tensor! Not numpy array!
        with torch.no_grad():
            x = to_cuda(maybe_to_torch(x), gpu_id=self.get_device())
            result_torch = torch.zeros([1, self.num_classes] + list(x.shape[2:]), dtype=torch.float).cuda(
                self.get_device(), non_blocking=True)
            mult = to_cuda(maybe_to_torch(mult), gpu_id=self.get_device())

            num_results = num_repeats
            if do_mirroring:
                mirror_idx = 8
                num_results *= 2 ** len(mirror_axes)
            else:
                mirror_idx = 1

            for i in range(num_repeats):
                for m in range(mirror_idx):
                    if m == 0:
                        output = self(x)
                        pred = self.inference_apply_nonlin(output[0] if isinstance(output, tuple) else output)
                        result_torch += 1 / num_results * pred

                    if m == 1 and (2 in mirror_axes):
                        output = self(flip(x, 4))
                        pred = self.inference_apply_nonlin(output[0] if isinstance(output, tuple) else output)
                        result_torch += 1 / num_results * flip(pred, 4)

                    if m == 2 and (1 in mirror_axes):
                        output = self(flip(x, 3))
                        pred = self.inference_apply_nonlin(output[0] if isinstance(output, tuple) else output)
                        result_torch += 1 / num_results * flip(pred, 3)

                    if m == 3 and (2 in mirror_axes) and (1 in mirror_axes):
                        output = self(flip(flip(x, 4), 3))
                        pred = self.inference_apply_nonlin(output[0] if isinstance(output, tuple) else output)
                        result_torch += 1 / num_results * flip(flip(pred, 4), 3)

                    if m == 4 and (0 in mirror_axes):
                        output = self(flip(x, 2))
                        pred = self.inference_apply_nonlin(output[0] if isinstance(output, tuple) else output)
                        result_torch += 1 / num_results * flip(pred, 2)

                    if m == 5 and (0 in mirror_axes) and (2 in mirror_axes):
                        output = self(flip(flip(x, 4), 2))
                        pred = self.inference_apply_nonlin(output[0] if isinstance(output, tuple) else output)
                        result_torch += 1 / num_results * flip(flip(pred, 4), 2)

                    if m == 6 and (0 in mirror_axes) and (1 in mirror_axes):
                        output = self(flip(flip(x, 3), 2))
                        pred = self.inference_apply_nonlin(output[0] if isinstance(output, tuple) else output)
                        result_torch += 1 / num_results * flip(flip(pred, 3), 2)

                    if m == 7 and (0 in mirror_axes) and (1 in mirror_axes) and (2 in mirror_axes):
                        output = self(flip(flip(flip(x, 3), 2), 4))
                        pred = self.inference_apply_nonlin(output[0] if isinstance(output, tuple) else output)
                        result_torch += 1 / num_results * flip(flip(flip(pred, 3), 2), 4)

            if mult is not None:
                result_torch[:, :] *= mult

        return result_torch

    def _internal_maybe_mirror_and_pred_2D(self, x, num_repeats, mirror_axes, do_mirroring=True, mult=None):
        # everything in here takes place on the GPU. If x and mult are not yet on GPU this will be taken care of here
        # we now return a cuda tensor! Not numpy array!
        with torch.no_grad():
            x = to_cuda(maybe_to_torch(x), gpu_id=self.get_device())
            mult = to_cuda(maybe_to_torch(mult), gpu_id=self.get_device())
            result_torch = torch.zeros([1, self.num_classes] + list(x.shape[2:]),
                                       dtype=torch.float).cuda(self.get_device(), non_blocking=True)

            num_results = num_repeats
            if do_mirroring:
                mirror_idx = 4
                num_results *= 2 ** len(mirror_axes)
            else:
                mirror_idx = 1

            for i in range(num_repeats):
                for m in range(mirror_idx):
                    if m == 0:
                        output = self(x)
                        pred = self.inference_apply_nonlin(output[0] if isinstance(output, tuple) else output)
                        result_torch += 1 / num_results * pred

                    if m == 1 and (1 in mirror_axes):
                        output = self(flip(x, 3))
                        pred = self.inference_apply_nonlin(output[0] if isinstance(output, tuple) else output)
                        result_torch += 1 / num_results * flip(pred, 3)

                    if m == 2 and (0 in mirror_axes):
                        output = self(flip(x, 2))
                        pred = self.inference_apply_nonlin(output[0] if isinstance(output, tuple) else output)
                        result_torch += 1 / num_results * flip(pred, 2)

                    if m == 3 and (0 in mirror_axes) and (1 in mirror_axes):
                        output = self(flip(flip(x, 3), 2))
                        pred = self.inference_apply_nonlin(output[0] if isinstance(output, tuple) else output)
                        result_torch += 1 / num_results * flip(flip(pred, 3), 2)

        if mult is not None:
            result_torch[:, :] *= mult

        return result_torch

    def predict_3D_pseudo3D_2Dconv(self, data, do_mirroring, num_repeats, min_size=None, BATCH_SIZE=None,
                                   mirror_axes=(0, 1), regions_class_order=None, pseudo3D_slices=5, all_in_gpu=False):
        if all_in_gpu:
            raise NotImplementedError
        assert len(data.shape) == 4, "data must be c, x, y, z"
        assert pseudo3D_slices % 2 == 1, "pseudo3D_slices must be odd"
        extra_slices = (pseudo3D_slices - 1) // 2
        shp_for_pad = np.array(data.shape)
        shp_for_pad[1] = extra_slices
        pad = np.zeros(shp_for_pad, dtype=np.float32)
        data = np.concatenate((pad, data, pad), 1)
        predicted_segmentation = []
        softmax_pred = []
        for s in range(extra_slices, data.shape[1] - extra_slices):
            d = data[:, (s - extra_slices):(s + extra_slices + 1)]
            d = d.reshape((-1, d.shape[-2], d.shape[-1]))
            pred_seg, bayesian_predictions, softmax_pres, uncertainty = \
                self._internal_predict_2D_2Dconv(d, do_mirroring, num_repeats, min_size, BATCH_SIZE, mirror_axes,
                                                 regions_class_order)
            predicted_segmentation.append(pred_seg[None])
            softmax_pred.append(softmax_pres[None])
        predicted_segmentation = np.vstack(predicted_segmentation)
        softmax_pred = np.vstack(softmax_pred).transpose((1, 0, 2, 3))

        return predicted_segmentation, None, softmax_pred, None

    def forward(self, x):
        x = hdc(x, self.device)
        x = self.first(x)
        x, conv1 = self.Conv_down1(x)
        x, conv2 = self.Conv_down2(x)
        x, conv3 = self.Conv_down3(x)
        _, x = self.Conv_down5(x)
        x = self.Conv_up2(x, conv3)
        x = self.Conv_up3(x, conv2)
        x = self.Conv_up4(x, conv1)

        seg_x = self.Conv_up5(x)
        seg_x = self.up(seg_x)
        seg_x = self.Conv_out(seg_x)

        # count_x = self.Conv_up6(x)
        # count_x = self.Conv_up7(count_x)
        # count_x = self.up_c(count_x)
        # count_x = self.Conv_out_c(count_x)
        seg_outputs = []
        seg_outputs.append(seg_x)
        return tuple(seg_outputs)


def count_param(model):
    param_count = 0
    for param in model.parameters():
        param_count += param.view(-1).size()[0]
    return param_count


if __name__ == "__main__":
    # 6716849
    # 6759522
    print(count_param(PGS_Net(5, 5, device='0')))
