import os
import sys
import PyInstaller.__main__

def build_exe():
    # 确保我们在正确的目录中
    script_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(script_dir)
    
    # PyInstaller参数
    args = [
        'schedule_display.py',  # 主程序文件
        '--name=课程表',  # 生成的exe文件名
        '--windowed',  # 不显示控制台窗口
        '--onefile',  # 打包成单个exe文件
        '--icon=NONE',  # 如果有图标文件，替换NONE为图标路径
        # 不再将schedule.xlsx打包进exe
        '--clean',  # 清理临时文件
        '--noconfirm',  # 不询问确认
    ]
    
    # 添加所需的隐式导入
    hidden_imports = [
        '--hidden-import=pandas',
        '--hidden-import=openpyxl',
    ]
    args.extend(hidden_imports)
    
    try:
        PyInstaller.__main__.run(args)
        print("打包完成！exe文件位于dist目录中。")
    except Exception as e:
        print(f"打包过程中出现错误：{e}")
        sys.exit(1)

if __name__ == '__main__':
    build_exe()
