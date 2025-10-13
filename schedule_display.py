import sys
import pandas as pd
from datetime import datetime
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout,
                            QTableWidget, QTableWidgetItem, QLabel, QFileDialog,
                            QPushButton, QMessageBox)
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QColor
import os

class ScheduleWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('课程表显示')
        self.setGeometry(100, 100, 800, 600)
        
        # 创建主窗口部件
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        
        # 创建文件选择按钮
        self.file_button = QPushButton('选择课程表文件')
        self.file_button.clicked.connect(self.select_file)
        layout.addWidget(self.file_button)
        
        # 创建日期和时间标签
        self.date_label = QLabel()
        self.time_label = QLabel()
        layout.addWidget(self.date_label)
        layout.addWidget(self.time_label)
        
        # 保存当前文件路径
        self.current_file = None
        
        # 创建课程表格
        self.table = QTableWidget()
        self.table.setColumnCount(2)
        self.table.setHorizontalHeaderLabels(['时间', '课程'])
        layout.addWidget(self.table)
        
        # 设置定时器更新时间
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_time)
        self.timer.start(1000)  # 每秒更新一次
        
        # 初始化数据
        self.schedule_data = None
        self.load_schedule()
        self.update_time()
        
    def select_file(self):
        file_name, _ = QFileDialog.getOpenFileName(
            self,
            "选择课程表文件",
            "",
            "Excel Files (*.xlsx *.xls);;All Files (*)"
        )
        if file_name:
            self.current_file = file_name
            self.load_schedule()
            
    def load_schedule(self):
        try:
            # 如果没有选择文件，尝试从默认位置读取
            if not self.current_file:
                default_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'schedule.xlsx')
                if os.path.exists(default_file):
                    self.current_file = default_file
                else:
                    QMessageBox.warning(self, "提示", "未找到默认课程表文件，请选择文件")
                    return
            
            # 读取Excel文件
            df = pd.read_excel(self.current_file)
            weekday = datetime.now().weekday()  # 0-6，0是周一
            
            # 获取对应星期的课程（第1列是周一，第3列是周二，以此类推）
            time_col = weekday * 2
            course_col = time_col + 1
            
            # 提取当天的时间和课程
            times = df.iloc[1:, time_col].tolist()
            courses = df.iloc[1:, course_col].tolist()
            
            # 更新表格
            self.table.setRowCount(len(times))
            for i, (time, course) in enumerate(zip(times, courses)):
                if pd.isna(time) or pd.isna(course):
                    continue
                time_item = QTableWidgetItem(str(time))
                course_item = QTableWidgetItem(str(course))
                self.table.setItem(i, 0, time_item)
                self.table.setItem(i, 1, course_item)
            
            # 调整列宽
            self.table.resizeColumnsToContents()
            
            self.schedule_data = list(zip(times, courses))
        except Exception as e:
            print(f"加载课程表出错: {e}")
    
    def update_time(self):
        current_time = datetime.now()
        weekdays = ['一', '二', '三', '四', '五', '六', '日']
        
        # 更新日期和时间标签
        self.date_label.setText(f'星期{weekdays[current_time.weekday()]}')
        self.time_label.setText(current_time.strftime('%H:%M:%S'))
        
        if self.schedule_data:
            self.highlight_next_class(current_time)
    
    def highlight_next_class(self, current_time):
        current_time_str = current_time.strftime('%H:%M')
        next_class_index = -1
        
        # 查找下一节课
        for i, (time_str, _) in enumerate(self.schedule_data):
            if pd.isna(time_str):
                continue
            # 处理时间范围格式 "18:00-19:00"
            try:
                start_time = str(time_str).split('-')[0].strip()
                if start_time > current_time_str:
                    next_class_index = i
                    break
            except:
                continue
        
        # 重置所有行的背景色
        for i in range(self.table.rowCount()):
            for j in range(2):
                item = self.table.item(i, j)
                if item:
                    item.setBackground(QColor(255, 255, 255))
        
        # 高亮下一节课
        if next_class_index != -1:
            for j in range(2):
                item = self.table.item(next_class_index, j)
                if item:
                    item.setBackground(QColor(255, 255, 0))  # 黄色高亮

def main():
    app = QApplication(sys.argv)
    window = ScheduleWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == '__main__':
    main()
