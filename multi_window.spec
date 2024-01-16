# -*- mode: python -*-
# _*_ coding:utf-8 _*_
import os
import sys

from PyInstaller.utils.hooks import collect_data_files

# If ITK is pip installed, gets all the files.
itk_datas = collect_data_files('itk', include_py_files=True)

block_cipher = None

# 当前路径
cur_path=os.path.abspath('.')
# python所在的路径
python_path=sys.path[4]
# 第三方包路径
packages_path=os.path.join(python_path,'Lib','site-packages')


models=[
    # 'models/nnUNet/nnUNetTrainerV2__nnUNetPlansv2.1',
    'models/CTPelvic1K/nnUNetTrainer__nnUNetPlans',
    'models/CTPelvic1K_CS_Net/nnUNetTrainer__nnUNetPlans',
    'models/classify'
]

# 需要的数据
datas=[
(os.path.join('resources','*'),'resources'),
(os.path.join('Operative/model','*'),'Operative/model'),
('models/Rib_Segment_HDC_Net/model_epoch_419_0.9307080876230142.pth','models/Rib_Segment_HDC_Net')
]

# ITK
datas += [x for x in itk_datas if '__pycache__' not in x[0]]

hidden_imports = ['sklearn.utils._typedefs']

for model in models:
    if os.path.isabs(model):
        model = os.path.abspath(model)
    model = os.path.relpath(model, cur_path)
    for root, dirs, files in os.walk(model):
        for file in files:
            datas.append((os.path.join(root, file), root))

a = Analysis(['multi_window.py'],
             pathex=[
             ],
             binaries=[],
             datas=datas,
             hiddenimports=hidden_imports,
             hookspath=[],
             hooksconfig={},
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)

exe = EXE(pyz,
          a.scripts, 
          [],
          exclude_binaries=True,
          name='multi_window',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          console=True,
          disable_windowed_traceback=False,
          target_arch=None,
          codesign_identity=None,
          entitlements_file=None )
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas, 
               strip=False,
               upx=True,
               upx_exclude=[],
               name='multi_window')
