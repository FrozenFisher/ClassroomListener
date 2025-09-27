import PyInstaller.__main__
import os

# PyInstaller配置
args = [
    'classroom_listener.py',
    '--onefile',  # 打包成单个exe文件
    '--windowed',  # 不显示控制台窗口
    '--name=ClassroomListener',  # 输出文件名
    '--icon=icon.ico',  # 图标文件（如果有的话）
    '--add-data=requirements.txt;.',  # 包含依赖文件
    '--hidden-import=pyaudio',
    '--hidden-import=numpy',
    '--hidden-import=tkinter',
    '--clean',  # 清理临时文件
]

# 如果没有图标文件，移除图标参数
if not os.path.exists('icon.ico'):
    args = [arg for arg in args if not arg.startswith('--icon')]

PyInstaller.__main__.run(args)
