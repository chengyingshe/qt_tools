import os
import sys
import matplotlib.pyplot as plt
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import pandas as pd

import numpy as np

plot_type_map = {0: '折线图', 1: '条形图', 2: '饼状图', 3: '直方图'}

class ChartWindow(QWidget):
    def __init__(self, ):
        super().__init__()

    def plot_and_show(self, col_data: pd.Series, plot_type: int):
        """绘制不同图形
        
        Keyword arguments:
        col_data -- 需要绘制的列数据
        plot_type -- 0：折线图，1：条形图，2：饼状图
        """
        title = plot_type_map[plot_type]
        self.setWindowTitle(title)
        data = col_data
        fig, ax = plt.subplots()
        if title == '折线图':
            ax.plot(data.index, data, label=data.name)
            ax.set_xlabel('index')
            ax.set_ylabel('value')
            ax.set_title('Line Graph')
            ax.legend()

        elif title == '条形图':
            ax.bar(np.arange(len(data)), data, width=0.3, align='center', label=data.name)
            ax.set_xticks(np.arange(len(data)) + 0.4)
            ax.set_xticklabels(data.index)
            ax.set_xlabel('index')
            ax.set_ylabel('value')
            ax.set_title('Bar Graph')
            ax.legend()

        elif title == '饼状图':
            data = data.fillna(0)  # 从列'A'读取数据
            data = data / data.sum() * 100
            ax.pie(data, labels=data.index, autopct='%1.1f%%')
            ax.set_title('Pie Chart')

        elif title == '直方图':
            ax.hist(data, bins=15)
            ax.set_xlabel('value')
            ax.set_ylabel('count')
            ax.set_title('Histogram')

        canvas = FigureCanvas(fig)
        layout = QVBoxLayout()
        layout.addWidget(canvas)
        self.setLayout(layout)
        super().show()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    file_path = os.path.join(os.path.dirname(__file__), 'table/test_length_not_same.csv')
    df = pd.read_csv(file_path)
    print(df.corrwith(df.index))
    chart_window = ChartWindow(df)
    chart_window.plot_and_show()
    sys.exit(app.exec_())