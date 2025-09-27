# -*- coding: utf-8 -*-
import tkinter as tk
from tkinter import ttk, messagebox
import threading
import time
import math
import json
import os
import sys

# 设置环境变量解决Windows中文编码问题
if sys.platform == "win32":
    os.environ['PYTHONIOENCODING'] = 'utf-8'

class SimpleClassroomListener:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("课堂分贝监控器 (简化版)")
        self.root.geometry("300x400")
        self.root.configure(bg='#2b2b2b')
        
        # 设置窗口置顶
        self.root.attributes('-topmost', True)
        
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
            font=("Microsoft YaHei", 16, "bold"),
            fg='white',
            bg='#2b2b2b'
        )
        title_label.pack(pady=10)
        
        # 当前分贝显示
        self.db_label = tk.Label(
            self.root,
            text="0 dB",
            font=("Microsoft YaHei", 24, "bold"),
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
            font=("Microsoft YaHei", 12),
            fg='white',
            bg='#2b2b2b'
        ).pack(side=tk.LEFT)
        
        self.threshold_var = tk.StringVar(value=str(self.threshold_db))
        threshold_entry = tk.Entry(
            threshold_frame,
            textvariable=self.threshold_var,
            width=10,
            font=("Microsoft YaHei", 12)
        )
        threshold_entry.pack(side=tk.LEFT, padx=5)
        
        tk.Label(
            threshold_frame,
            text="dB",
            font=("Microsoft YaHei", 12),
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
            font=("Microsoft YaHei", 12),
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
            font=("Microsoft YaHei", 12),
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
            font=("Microsoft YaHei", 10),
            fg='yellow',
            bg='#2b2b2b'
        )
        self.status_label.pack(pady=5)
        
        # 说明文本
        info_label = tk.Label(
            self.root,
            text="注意: 这是简化版本，\n使用模拟数据演示功能",
            font=("Microsoft YaHei", 9),
            fg='orange',
            bg='#2b2b2b'
        )
        info_label.pack(pady=10)
        
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
            
            # 开始监控
            self.is_monitoring = True
            self.monitor_thread = threading.Thread(target=self.simulate_audio)
            self.monitor_thread.daemon = True
            self.monitor_thread.start()
            
            # 更新UI状态
            self.start_button.config(state=tk.DISABLED)
            self.stop_button.config(state=tk.NORMAL)
            self.status_label.config(text="状态: 监控中 (模拟)", fg='green')
            
        except Exception as e:
            messagebox.showerror("错误", f"启动监控失败: {str(e)}")
            
    def stop_monitoring(self):
        self.is_monitoring = False
        
        # 更新UI状态
        self.start_button.config(state=tk.NORMAL)
        self.stop_button.config(state=tk.DISABLED)
        self.status_label.config(text="状态: 已停止", fg='red')
        
        # 重置显示
        self.current_db = 0
        self.db_label.config(text="0 dB")
        self.update_db_bar(0)
        
    def simulate_audio(self):
        """模拟音频数据（用于演示）"""
        import random
        
        while self.is_monitoring:
            try:
                # 模拟分贝值（30-90之间随机变化）
                base_db = 50 + random.randint(-20, 40)
                # 添加一些随机波动
                db = base_db + random.randint(-5, 5)
                db = max(0, min(100, db))  # 限制在0-100范围内
                    
                self.current_db = db
                
                # 更新UI（在主线程中）
                self.root.after(0, self.update_display, db)
                
                # 检查阈值
                if db > self.threshold_db:
                    self.root.after(0, self.show_alert, db)
                    
                time.sleep(0.1)  # 100ms更新一次
                    
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
            font=("Microsoft YaHei", 16, "bold"),
            fg='white',
            bg='#ff4444'
        ).pack(pady=20)
        
        tk.Label(
            alert_window,
            text=f"当前分贝: {db:.1f} dB",
            font=("Microsoft YaHei", 14),
            fg='white',
            bg='#ff4444'
        ).pack()
        
        tk.Label(
            alert_window,
            text=f"阈值: {self.threshold_db} dB",
            font=("Microsoft YaHei", 12),
            fg='white',
            bg='#ff4444'
        ).pack(pady=5)
        
        # 关闭按钮
        tk.Button(
            alert_window,
            text="确定",
            command=alert_window.destroy,
            font=("Microsoft YaHei", 12),
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
    app = SimpleClassroomListener()
    app.run()
