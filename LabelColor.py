#!/usr/bin/env python
# _*_ coding:utf-8 _*_
import random

import numpy as np


class LabelColor:
    label2r = {1: 0, 2: 255, 3: 0, 4: 255, 5: 0, 6: 255}
    label2g = {1: 0, 2: 0, 3: 255, 4: 255, 5: 255, 6: 0}
    label2b = {1: 255, 2: 0, 3: 0, 4: 0, 5: 255, 6: 255}
    label2description = {1: 'Label 1', 2: 'Label 2', 3: 'Label 3', 4: 'Label 4', 5: 'Label 5', 6: 'Label 6'}
    rgb2label_dict = {0: 0, 0x0000FF: 1, 0xFF0000: 2, 0x00FF00: 3, 0xFFFF00: 4, 0x00FFFF: 5, 0xFF00FF: 6}
    rgb2label_func = np.vectorize(rgb2label_dict.get)

    @staticmethod
    def reset():
        LabelColor.label2r = {1: 0, 2: 255, 3: 0, 4: 255, 5: 0, 6: 255}
        LabelColor.label2g = {1: 0, 2: 0, 3: 255, 4: 255, 5: 255, 6: 0}
        LabelColor.label2b = {1: 255, 2: 0, 3: 0, 4: 0, 5: 255, 6: 255}
        LabelColor.label2description = {1: 'Label 1', 2: 'Label 2', 3: 'Label 3',
                                        4: 'Label 4', 5: 'Label 5', 6: 'Label 6'}
        LabelColor.rgb2label_dict = {0: 0, 0x0000FF: 1, 0xFF0000: 2, 0x00FF00: 3, 0xFFFF00: 4, 0x00FFFF: 5, 0xFF00FF: 6}
        LabelColor.rgb2label_func = np.vectorize(LabelColor.rgb2label_dict.get)

    @staticmethod
    def to_file(path):
        with open(path, 'w') as f:
            f.write('################################################\n')
            f.write('# ITK-SnAP Label Description File\n')
            f.write('# File format: \n')
            f.write('# IDX   -R-  -G-  -B-  LABEL\n')
            # f.write('# IDX   -R-  -G-  -B-  -A--  VIS MSH  LABEL\n')
            f.write('# Fields: \n')
            f.write('#    IDX:   Zero-based index \n')
            f.write('#    -R-:   Red color component (0..255)\n')
            f.write('#    -G-:   Green color component (0..255)\n')
            f.write('#    -B-:   Blue color component (0..255)\n')
            # f.write('#    -A-:   Label transparency (0.00 .. 1.00)\n')
            # f.write('#    VIS:   Label visibility (0 or 1)\n')
            # f.write('#    IDX:   Label mesh visibility (0 or 1)\n')
            f.write('#  LABEL:   Label description \n')
            f.write('################################################\n')
            for k in LabelColor.label2r.keys():
                f.write(
                    f'\t{k}\t{LabelColor.label2r[k]}\t{LabelColor.label2g[k]}\t{LabelColor.label2b[k]}\t{LabelColor.label2description[k]}\n')

    @staticmethod
    def read_file(path):
        temp_label2r = {}
        temp_label2g = {}
        temp_label2b = {}
        temp_label2description = {}
        temp_rgb2label_dict = {}
        for line in open(path, 'r'):
            line = line.strip()
            if '' == line or line.startswith('#'):
                continue
            k, r, g, b, d = line.split('\t')
            k = int(k)
            r = int(r)
            g = int(g)
            b = int(b)
            temp_label2r[k] = r
            temp_label2g[k] = g
            temp_label2b[k] = b
            temp_label2description[k] = d
            temp_rgb2label_dict[r << 16 | g << 8 | b] = k
        LabelColor.label2r = temp_label2r
        LabelColor.label2g = temp_label2g
        LabelColor.label2b = temp_label2b
        LabelColor.label2description = temp_label2description
        LabelColor.rgb2label_dict = temp_rgb2label_dict
        # rgb转gray
        LabelColor.rgb2label_func = np.vectorize(LabelColor.rgb2label_dict.get)

    @staticmethod
    def fill_all():
        all_colors = list(set(range(1, 1 + 0xffffff)) - LabelColor.rgb2label_dict.keys())
        x = len(LabelColor.rgb2label_dict) - 1
        all_colors = random.sample(all_colors, 255 - x)
        for c in all_colors:
            x += 1
            r = c >> 16
            g = (c >> 8) & 0xff
            b = c & 0xff
            LabelColor.label2r[x] = r
            LabelColor.label2g[x] = g
            LabelColor.label2b[x] = b
            LabelColor.rgb2label_dict[c] = x
            # rgb转gray
            LabelColor.rgb2label_func = np.vectorize(LabelColor.rgb2label_dict.get)

    @staticmethod
    def rgb2label(img):
        return LabelColor.rgb2label_func(img).astype(np.uint8)


if __name__ == '__main__':
    LabelColor.to_file('test.txt')
