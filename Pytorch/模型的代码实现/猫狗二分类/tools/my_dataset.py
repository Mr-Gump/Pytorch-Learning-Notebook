# -*- coding: utf-8 -*-
"""
# @file name  : dataset.py
# @author     : yts3221@126.com
# @date       : 2019-08-21 10:08:00
# @brief      : 各数据集的Dataset定义
"""

import os
import random
from PIL import Image
from torch.utils.data import Dataset

random.seed(1)
dc_label = {"cat": 0, "dog": 1}    # 标签设定


class DCDataset(Dataset):
    def __init__(self, data_dir, transform=None):
        """
        猫狗分类任务的Dataset
        :param data_dir: str, 数据集所在路径
        :param transform: torch.transform，数据预处理
        """
        self.label_name = {"cat": 0, "dog": 1}    # 标签设定
        self.data_info = self.get_img_info(data_dir)  # data_info存储所有图片路径和标签，在DataLoader中通过index读取样本
        self.transform = transform

    # 将图片transform后返回图片和标签
    def __getitem__(self, index):
        path_img, label = self.data_info[index]
        img = Image.open(path_img).convert('RGB')     # 0~255

        if self.transform is not None:
            img = self.transform(img)   # 在这里做transform，转为tensor等等

        return img, label

    def __len__(self):
        return len(self.data_info)

    @staticmethod
    # 读取图片和对应标签,返回图片和标签元组的列表
    def get_img_info(data_dir):
        data_info = list()
        for root, dirs, _ in os.walk(data_dir):
            # 遍历类别
            for sub_dir in dirs:
                img_names = os.listdir(os.path.join(root, sub_dir))
                img_names = list(filter(lambda x: x.endswith('.jpg'), img_names))

                # 遍历图片
                for i in range(len(img_names)):
                    img_name = img_names[i]
                    path_img = os.path.join(root, sub_dir, img_name)
                    label = dc_label[sub_dir]
                    data_info.append((path_img, int(label)))

        return data_info
