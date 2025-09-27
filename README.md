# 课堂分贝监控器 (ClassroomListener)

一个Windows系统级置顶的分贝监控程序，可以实时监控麦克风输入的分贝大小，并在超过设定阈值时弹出警告。

## 功能特性

- 🎤 **实时麦克风监控**: 通过麦克风输入获取当前环境分贝大小
- 📊 **可视化分贝条**: 从下往上由绿到红的分贝条显示
- 🔢 **数字显示**: 实时显示当前分贝数值
- ⚠️ **阈值警告**: 超过设定分贝阈值时弹出警告窗口
- 🔝 **系统级置顶**: 窗口始终保持在最前面
- 💾 **配置保存**: 自动保存阈值设置
- 📦 **单文件执行**: 打包成单个exe文件，无需安装

## 版本说明

### 完整版本 (ClassroomListener.exe)
- 使用真实的麦克风输入
- 需要PyAudio库支持
- 功能完整，适合实际使用

### 简化版本 (ClassroomListener-Simple.exe)
- 使用模拟数据演示功能
- 无需额外依赖，构建简单
- 适合演示和测试界面功能

## 系统要求

- Windows 10/11
- 麦克风设备（仅完整版本需要）
- Python 3.9+ (仅开发环境需要)

## 下载使用

1. 进入[Releases页面](https://github.com/FrozenFisher/ClassroomListener/releases)
2. 下载最新版本：
   - `ClassroomListener.exe` - 完整版本（推荐）
   - `ClassroomListener-Simple.exe` - 简化版本（演示用）
3. 双击运行程序
4. 设置分贝阈值（默认70dB）
5. 点击"开始监控"按钮

## 使用方法

1. **设置阈值**: 在"阈值设置"框中输入期望的分贝阈值
2. **开始监控**: 点击"开始监控"按钮开始实时监控
3. **查看分贝**: 观察顶部的数字显示和下方的分贝条
4. **接收警告**: 当分贝超过阈值时，会弹出警告窗口
5. **停止监控**: 点击"停止监控"按钮停止监控

## 界面说明

- **分贝显示**: 顶部显示当前分贝数值
- **分贝条**: 颜色从绿色（低分贝）渐变到红色（高分贝）
- **阈值设置**: 可自定义警告阈值
- **控制按钮**: 开始/停止监控
- **状态显示**: 显示当前监控状态

## 开发环境搭建

如果需要从源码构建：

```bash
# 克隆仓库
git clone https://github.com/FrozenFisher/ClassroomListener.git
cd ClassroomListener

# 构建完整版本
python install_deps.py  # 智能安装依赖
python build_exe.py     # 构建完整版本

# 构建简化版本
pip install pyinstaller
python build_simple.py  # 构建简化版本
```

## 自动构建

项目使用GitHub Actions自动构建：

- 推送标签时自动触发构建
- 同时构建完整版本和简化版本
- 自动创建Release并上传exe文件

### 触发构建
```bash
# 创建标签
git tag v1.0.0
git push origin v1.0.0
```

## 技术栈

- **GUI框架**: tkinter
- **音频处理**: pyaudio (完整版本)
- **数值计算**: numpy (完整版本)
- **打包工具**: PyInstaller

## 故障排除

### PyAudio安装问题
如果遇到PyAudio编译错误，可以：
1. 使用简化版本进行演示
2. 手动安装预编译的PyAudio wheel包
3. 使用conda安装：`conda install pyaudio`

### 麦克风权限
- 首次运行可能需要授予麦克风权限
- 确保麦克风设备正常工作
- 检查Windows音频设置

### 杀毒软件误报
- exe文件可能被杀毒软件误报
- 这是PyInstaller打包的常见情况
- 可以添加到白名单或使用简化版本

## 版本历史

- v1.0.0: 初始版本，包含基本的分贝监控和警告功能
- 添加简化版本支持，解决PyAudio编译问题

## 许可证

MIT License
