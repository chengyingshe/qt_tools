import sys
import matplotlib.pyplot as plt
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas


class ChartWindow(QWidget):
    def __init__(self, df_data):
        super().__init__()
        self.setWindowTitle('Bar Chart Window')

        data = df_data
        A = data['A']  # 从列'A'读取数据
        B = data['B']  # 从列'B'读取数据
        C = data['C']  # 从列'C'读取数据
        # 绘制折线图
        fig, ax = plt.subplots()
        ax.plot(data.index, A, label='A')
        ax.plot(data.index, B, label='B')
        ax.plot(data.index, C, label='C')
        ax.set_xlabel('index')
        ax.set_ylabel('value')
        ax.set_title('Line Graph')
        ax.legend()

        # 创建FigureCanvasQTAgg对象，将图表嵌入到PyQt5的界面中
        canvas = FigureCanvas(fig)

        # 清除之前的图表（如果有），并添加新的图表
        layout = QVBoxLayout()
        layout.addWidget(canvas)
        self.setLayout(layout)