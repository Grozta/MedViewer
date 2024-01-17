# 骨科医学影像智能处理平台

Python3.7.10  
安装pytorch>=1.7.1

然后
```Bash

# 先安装torch
# CPU only
pip install torch==1.13.0+cpu torchvision==0.14.0+cpu torchaudio==0.13.0 --extra-index-url https://download.pytorch.org/whl/cpu
# 然后SimpleITK
conda install -c conda-forge simpleitk
# opencv安装旧版本
pip install opencv-python==4.3.0.36
# 最后安装其他依赖
pip install -r requirements.txt
```

## 模型

链接：https://pan.baidu.com/s/1NoJ3UDLqvn5QXwebTpl_hw  
提取码：pltl 

直接解压到项目里

## 模型+测试数据

链接：https://pan.baidu.com/s/1LVT8ykSkq0nWRPj7Sah97g 
提取码：x8hz 

直接解压到项目里

## 打包

(只在自己电脑测过)  
安装

```Bash
pip install pyinstaller
```

然后

```Bash
pyinstaller multi_window.spec
```