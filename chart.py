import os
import sys
import matplotlib.pyplot as plt
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import pandas as pd


class ChartWindow(QWidget):
    def __init__(self, df_data: pd.DataFrame):
        super().__init__()
        self.setWindowTitle('折线图')
        fig, ax = plt.subplots()
        for col in df_data.columns:
            # 绘制折线图
            col_data = df_data[col]
            ax.plot(range(len(col_data)), col_data, label=col)
            
        ax.set_xlabel('Index')
        ax.set_ylabel('Value')
        ax.set_title('Line Graph')
        ax.legend()


        # 创建FigureCanvasQTAgg对象，将图表嵌入到PyQt5的界面中
        canvas = FigureCanvas(fig)

        # 清除之前的图表（如果有），并添加新的图表
        layout = QVBoxLayout()
        layout.addWidget(canvas)
        self.setLayout(layout)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    file_path = os.path.join(os.path.dirname(__file__), 'table/test_length_not_same.csv')
    df = pd.read_csv(file_path)
    print(df.corrwith(df.index))
    chart_window = ChartWindow(df)
    chart_window.show()
    sys.exit(app.exec_())