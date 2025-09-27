# -*- coding: utf-8 -*-
import subprocess
import sys
import platform
import os

# 设置环境变量解决Windows中文编码问题
if sys.platform == "win32":
    os.environ['PYTHONIOENCODING'] = 'utf-8'
    # 设置控制台代码页为UTF-8
    try:
        os.system("chcp 65001 > nul 2>&1")
    except:
        pass

def install_pyaudio():
    """安装pyaudio，使用预编译的wheel包"""
    python_version = f"{sys.version_info.major}{sys.version_info.minor}"
    architecture = "win_amd64" if platform.machine().endswith('64') else "win32"
    
    # 尝试不同的预编译wheel包
    wheel_urls = [
        f"https://download.lfd.uci.edu/pythonlibs/archived/PyAudio-0.2.11-cp{python_version}-cp{python_version}-{architecture}.whl",
        f"https://files.pythonhosted.org/packages/ab/42/b4f04721c5c5bfc196ce156b3c768998ef8c0ae3654ed29ea5220c814a65/PyAudio-0.2.11-cp{python_version}-cp{python_version}-{architecture}.whl"
    ]
    
    for url in wheel_urls:
        try:
            print(f"尝试安装: {url}")
            subprocess.check_call([sys.executable, "-m", "pip", "install", url])
            print("PyAudio安装成功!")
            return True
        except subprocess.CalledProcessError:
            print(f"安装失败: {url}")
            continue
    
    # 如果预编译包都失败，尝试从源码安装
    try:
        print("尝试从源码安装PyAudio...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pyaudio"])
        print("PyAudio从源码安装成功!")
        return True
    except subprocess.CalledProcessError:
        print("PyAudio安装失败!")
        return False

def install_other_deps():
    """安装其他依赖"""
    deps = ["numpy==1.24.3", "pyinstaller==5.13.2"]
    
    for dep in deps:
        try:
            print(f"安装 {dep}...")
            subprocess.check_call([sys.executable, "-m", "pip", "install", dep])
            print(f"{dep} 安装成功!")
        except subprocess.CalledProcessError:
            print(f"{dep} 安装失败!")

if __name__ == "__main__":
    print("开始安装依赖...")
    
    # 升级pip
    subprocess.check_call([sys.executable, "-m", "pip", "install", "--upgrade", "pip"])
    
    # 安装PyAudio
    if install_pyaudio():
        # 安装其他依赖
        install_other_deps()
        print("所有依赖安装完成!")
    else:
        print("PyAudio安装失败，请手动安装")
        sys.exit(1)
