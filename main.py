import os
import sys

import numpy as np
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QPushButton, QVBoxLayout
from PyQt5.uic import loadUi
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import pandas as pd
from chart import ChartWindow

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.cur_dir = os.path.dirname(__file__)
        self.input_path = None
        self.output_dir = None
        self.df_data = None
        self.filled_df_data = None
        self.data_has_nan = False
        self.set_ui()
        self.__init_widgets()
        self.__bind_all_functions()
        
    def set_ui(self):
        ui_path = os.path.join(self.cur_dir, 'gui.ui')
        loadUi(ui_path, self)

    def __init_widgets(self):
        self.hasNanLabel.setVisible(False)

    def select_input_path_dialog(self, event):
        options = QFileDialog.Options()
        path, _ = QFileDialog.getOpenFileName(self,
                                              "选择导入文件",
                                              os.path.join(self.cur_dir, 'table'),
                                              "CSV Files (*.csv);;All Files (*)",
                                              options=options)
        if path:
            print(f"selected file: {path}")
            self.inputPathEdit.setText(path)
            self.input_path = path
            self.df_data = pd.read_csv(self.input_path)
            self.filled_df_data = self.df_data
            self.__check_df_data_if_has_nan()

    def __check_df_data_if_has_nan(self):
        if self.df_data is None or self.df_data.isnull().values.any():
            print('数据中存在缺失值')
            self.hasNanLabel.setVisible(True)
            self.data_has_nan = True
        else:
            self.data_has_nan = False

    def fill_data(self):
        # TODO: 填充缺失值
        if self.df_data is not None and self.data_has_nan:
            if self.dataFillType.currentText() == '平均数':
                fill_val = self.df_data.mean()
            elif self.dataFillType.currentText() == '中位数':
                fill_val = self.df_data.median()
            elif self.dataFillType.currentText() == '众数':
                fill_val = self.df_data.mode()
            self.filled_df_data = self.df_data.fillna(fill_val)
            self.data_has_nan = False
            self.hasNanLabel.setVisible(False)

            print(f'利用数据特征【{self.dataFillType.currentText()}】填充成功！')


    def select_output_dir_dialog(self, event):
        # TODO: 选择导出文件夹路径
        directory = QFileDialog.getExistingDirectory(self, 
                                                     "选择导出文件夹", 
                                                     self.cur_dir, 
                                                     QFileDialog.ShowDirsOnly | QFileDialog.DontResolveSymlinks)
        if directory:
            print(f"selected dir: {directory}")
            self.outputDirEdit.setText(directory)
            self.output_dir = directory
            
    def output_csv_file(self):
        os.makedirs(self.output_dir, exist_ok=True)
        file_name = os.path.basename(self.input_path)
        file_name = os.path.splitext(file_name)[0] + '_filled.csv'
        output_path = os.path.join(self.output_dir, file_name)
        self.filled_df_data.to_csv(output_path, index=False)
        print(f'成功导出文件：{output_path}')

    def visualize(self):
        # TODO: 可视化图表功能实现
        if self.df_data is not None and not self.data_has_nan:
            print('可视化数据：')
            print(self.filled_df_data)
            self.chart_window = ChartWindow(self.filled_df_data)
            self.chart_window.show()
        else:
            print('未导入CSV文件或数据存在缺失，无法可视化')

    def __bind_all_functions(self):
        self.inputPathEdit.mousePressEvent = self.select_input_path_dialog
        self.outputDirEdit.mousePressEvent = self.select_output_dir_dialog
        self.visualizeBtn.clicked.connect(self.visualize)
        self.dataFillBtn.clicked.connect(self.fill_data)
        self.outputBtn.clicked.connect(self.output_csv_file)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
