import tkinter as tk
from tkinter import ttk, messagebox
import pyaudio
import numpy as np
import threading
import time
import math
import json
import os

class ClassroomListener:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("课堂分贝监控器")
        self.root.geometry("300x400")
        self.root.configure(bg='#2b2b2b')
        
        # 设置窗口置顶
        self.root.attributes('-topmost', True)
        
        # 音频参数
        self.CHUNK = 1024
        self.FORMAT = pyaudio.paInt16
        self.CHANNELS = 1
        self.RATE = 44100
        self.p = None
        self.stream = None
        
        # 分贝相关变量
        self.current_db = 0
        self.max_db = 100
        self.threshold_db = 70  # 默认阈值
        self.is_monitoring = False
        self.monitor_thread = None
        
        # 配置文件名
        self.config_file = "config.json"
        
        # 加载配置
        self.load_config()
        
        # 创建GUI
        self.create_gui()
        
        # 绑定关闭事件
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        
    def create_gui(self):
        # 主标题
        title_label = tk.Label(
            self.root, 
            text="课堂分贝监控器", 
            font=("Arial", 16, "bold"),
            fg='white',
            bg='#2b2b2b'
        )
        title_label.pack(pady=10)
        
        # 当前分贝显示
        self.db_label = tk.Label(
            self.root,
            text="0 dB",
            font=("Arial", 24, "bold"),
            fg='white',
            bg='#2b2b2b'
        )
        self.db_label.pack(pady=10)
        
        # 分贝条
        self.create_db_bar()
        
        # 阈值设置
        threshold_frame = tk.Frame(self.root, bg='#2b2b2b')
        threshold_frame.pack(pady=10)
        
        tk.Label(
            threshold_frame,
            text="阈值设置:",
            font=("Arial", 12),
            fg='white',
            bg='#2b2b2b'
        ).pack(side=tk.LEFT)
        
        self.threshold_var = tk.StringVar(value=str(self.threshold_db))
        threshold_entry = tk.Entry(
            threshold_frame,
            textvariable=self.threshold_var,
            width=10,
            font=("Arial", 12)
        )
        threshold_entry.pack(side=tk.LEFT, padx=5)
        
        tk.Label(
            threshold_frame,
            text="dB",
            font=("Arial", 12),
            fg='white',
            bg='#2b2b2b'
        ).pack(side=tk.LEFT)
        
        # 控制按钮
        button_frame = tk.Frame(self.root, bg='#2b2b2b')
        button_frame.pack(pady=20)
        
        self.start_button = tk.Button(
            button_frame,
            text="开始监控",
            command=self.start_monitoring,
            font=("Arial", 12),
            bg='#4CAF50',
            fg='white',
            padx=20,
            pady=5
        )
        self.start_button.pack(side=tk.LEFT, padx=5)
        
        self.stop_button = tk.Button(
            button_frame,
            text="停止监控",
            command=self.stop_monitoring,
            font=("Arial", 12),
            bg='#f44336',
            fg='white',
            padx=20,
            pady=5,
            state=tk.DISABLED
        )
        self.stop_button.pack(side=tk.LEFT, padx=5)
        
        # 状态显示
        self.status_label = tk.Label(
            self.root,
            text="状态: 未开始",
            font=("Arial", 10),
            fg='yellow',
            bg='#2b2b2b'
        )
        self.status_label.pack(pady=5)
        
    def create_db_bar(self):
        # 分贝条框架
        bar_frame = tk.Frame(self.root, bg='#2b2b2b')
        bar_frame.pack(pady=10)
        
        # 分贝条背景
        self.bar_canvas = tk.Canvas(
            bar_frame,
            width=200,
            height=20,
            bg='#1a1a1a',
            highlightthickness=0
        )
        self.bar_canvas.pack()
        
        # 绘制分贝条
        self.update_db_bar(0)
        
    def update_db_bar(self, db_value):
        self.bar_canvas.delete("all")
        
        # 计算填充比例
        fill_ratio = min(db_value / self.max_db, 1.0)
        fill_width = int(200 * fill_ratio)
        
        # 根据分贝值选择颜色（绿色到红色渐变）
        if db_value < 30:
            color = '#00ff00'  # 绿色
        elif db_value < 50:
            color = '#80ff00'  # 黄绿色
        elif db_value < 70:
            color = '#ffff00'  # 黄色
        elif db_value < 85:
            color = '#ff8000'  # 橙色
        else:
            color = '#ff0000'  # 红色
            
        # 绘制填充条
        if fill_width > 0:
            self.bar_canvas.create_rectangle(
                0, 0, fill_width, 20,
                fill=color,
                outline=""
            )
            
    def start_monitoring(self):
        try:
            # 更新阈值
            self.threshold_db = float(self.threshold_var.get())
            self.save_config()
            
            # 初始化音频
            self.p = pyaudio.PyAudio()
            self.stream = self.p.open(
                format=self.FORMAT,
                channels=self.CHANNELS,
                rate=self.RATE,
                input=True,
                frames_per_buffer=self.CHUNK
            )
            
            # 开始监控
            self.is_monitoring = True
            self.monitor_thread = threading.Thread(target=self.monitor_audio)
            self.monitor_thread.daemon = True
            self.monitor_thread.start()
            
            # 更新UI状态
            self.start_button.config(state=tk.DISABLED)
            self.stop_button.config(state=tk.NORMAL)
            self.status_label.config(text="状态: 监控中", fg='green')
            
        except Exception as e:
            messagebox.showerror("错误", f"启动监控失败: {str(e)}")
            
    def stop_monitoring(self):
        self.is_monitoring = False
        
        if self.stream:
            self.stream.stop_stream()
            self.stream.close()
        if self.p:
            self.p.terminate()
            
        # 更新UI状态
        self.start_button.config(state=tk.NORMAL)
        self.stop_button.config(state=tk.DISABLED)
        self.status_label.config(text="状态: 已停止", fg='red')
        
        # 重置显示
        self.current_db = 0
        self.db_label.config(text="0 dB")
        self.update_db_bar(0)
        
    def monitor_audio(self):
        while self.is_monitoring:
            try:
                # 读取音频数据
                data = self.stream.read(self.CHUNK, exception_on_overflow=False)
                
                # 转换为numpy数组
                audio_data = np.frombuffer(data, dtype=np.int16)
                
                # 计算RMS值
                rms = np.sqrt(np.mean(audio_data**2))
                
                # 转换为分贝值
                if rms > 0:
                    db = 20 * math.log10(rms / 32767.0) + 100  # 调整到0-100范围
                    db = max(0, min(100, db))  # 限制在0-100范围内
                else:
                    db = 0
                    
                self.current_db = db
                
                # 更新UI（在主线程中）
                self.root.after(0, self.update_display, db)
                
                # 检查阈值
                if db > self.threshold_db:
                    self.root.after(0, self.show_alert, db)
                    
            except Exception as e:
                print(f"监控错误: {e}")
                break
                
    def update_display(self, db):
        self.db_label.config(text=f"{db:.1f} dB")
        self.update_db_bar(db)
        
    def show_alert(self, db):
        # 创建警告窗口
        alert_window = tk.Toplevel(self.root)
        alert_window.title("分贝警告")
        alert_window.geometry("300x150")
        alert_window.configure(bg='#ff4444')
        alert_window.attributes('-topmost', True)
        
        # 警告内容
        tk.Label(
            alert_window,
            text="⚠️ 分贝过高警告 ⚠️",
            font=("Arial", 16, "bold"),
            fg='white',
            bg='#ff4444'
        ).pack(pady=20)
        
        tk.Label(
            alert_window,
            text=f"当前分贝: {db:.1f} dB",
            font=("Arial", 14),
            fg='white',
            bg='#ff4444'
        ).pack()
        
        tk.Label(
            alert_window,
            text=f"阈值: {self.threshold_db} dB",
            font=("Arial", 12),
            fg='white',
            bg='#ff4444'
        ).pack(pady=5)
        
        # 关闭按钮
        tk.Button(
            alert_window,
            text="确定",
            command=alert_window.destroy,
            font=("Arial", 12),
            bg='white',
            fg='#ff4444',
            padx=20
        ).pack(pady=10)
        
        # 3秒后自动关闭
        alert_window.after(3000, alert_window.destroy)
        
    def load_config(self):
        try:
            if os.path.exists(self.config_file):
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    config = json.load(f)
                    self.threshold_db = config.get('threshold_db', 70)
        except Exception as e:
            print(f"加载配置失败: {e}")
            
    def save_config(self):
        try:
            config = {
                'threshold_db': self.threshold_db
            }
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(config, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"保存配置失败: {e}")
            
    def on_closing(self):
        self.stop_monitoring()
        self.save_config()
        self.root.destroy()
        
    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = ClassroomListener()
    app.run()
