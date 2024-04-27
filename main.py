import os
import sys

import numpy as np
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QPushButton, QVBoxLayout
from PyQt5.uic import loadUi
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import pandas as pd

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.cur_dir = os.path.dirname(__file__)
        self.input_path = None
        self.output_dir = None
        self.df_data = None
        self.set_ui()
        self.__init_widgets()
        self.__bind_all_functions()
        
    def set_ui(self):
        ui_path = os.path.join(self.cur_dir, 'gui.ui')
        loadUi(ui_path, self)

    def __init_widgets(self):
        pass

    def select_input_path_dialog(self, event):
        # TODO: 选择导入csv文件
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


    def visualize(self):
        # TODO: 可视化图表功能实现
        pass

    def __bind_all_functions(self):
        self.inputPathEdit.mousePressEvent = self.select_input_path_dialog
        self.outputDirEdit.mousePressEvent = self.select_output_dir_dialog
        self.visualizeBtn.clicked.connect(self.visualize)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
