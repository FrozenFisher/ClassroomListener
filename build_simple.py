import PyInstaller.__main__
import os

# 简化的PyInstaller配置（不需要pyaudio）
args = [
    'classroom_listener_simple.py',
    '--onefile',  # 打包成单个exe文件
    '--windowed',  # 不显示控制台窗口
    '--name=ClassroomListener-Simple',  # 输出文件名
    '--clean',  # 清理临时文件
]

PyInstaller.__main__.run(args)
