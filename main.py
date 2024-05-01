import os
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, \
                    QPushButton, QVBoxLayout, QTableWidget, QTableWidgetItem
from PyQt5.QtGui import QIntValidator
from PyQt5.uic import loadUi
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import pandas as pd
from chart import ChartWindow
import numpy as np
from predictor import Predictor

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.cur_dir = os.path.dirname(__file__)
        self.input_path = None
        self.output_dir = None
        self.df_data = None
        self.filled_df_data = None
        self.data_has_nan = False
        self.predictors = {}
        self.set_ui()
        self.__init_widgets()
        self.__bind_all_functions()
        
    def set_ui(self):
        ui_path = os.path.join(self.cur_dir, 'gui.ui')
        loadUi(ui_path, self)

    def __init_widgets(self):
        self.hasNanLabel.setVisible(False)
        self.predictNumEdit.setValidator(QIntValidator())  # 设置进能输入整数

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
            self.show_data()

    def show_data(self):
        if self.df_data is not None:
            self.__show_data_in_data_table()
            if not self.data_has_nan:  # 当数据不缺失时才用模型拟合
                self.__show_corr_in_corr_list()

    def __show_corr_in_corr_list(self):
        data = self.filled_df_data
        self.corrList.clear()
        self.corr = data.corrwith(pd.Series(data.index))
        # 添加数据到 corrList
        for key, value in self.corr.items():
            item = f'{key}: {value:.3f}'
            is_linear = abs(value) > 0.5
            item += '\t' + ('(线性)' if is_linear else '(非线性)')
            self.predictors[key] = Predictor(is_linear)
            score = self.predictors[key].fit(data[key])
            item += f'\t(模型拟合程度：{score * 100:.1f}%)'
            self.corrList.addItem(item)  # 格式化为浮点数，保留6位小数

    def __show_data_in_data_table(self):
        # 将csv表格中的数据展示在dataTable组件中
        data = self.filled_df_data
        self.dataTable.clear()
        self.dataTable.setRowCount(data.shape[0])
        self.dataTable.setColumnCount(data.shape[1])
        self.dataTable.setHorizontalHeaderLabels(data.columns)
        # 填充表格数据
        for index, row in data.iterrows():
            for column_index, value in enumerate(row):
                item = QTableWidgetItem(str(value) if not pd.isna(value) else '')
                self.dataTable.setItem(index, column_index, item)

    def __check_df_data_if_has_nan(self):
        if self.df_data is None or self.df_data.isnull().values.any():
            print('数据中存在缺失值')
            self.hasNanLabel.setVisible(True)
            self.data_has_nan = True
        else:
            self.hasNanLabel.setVisible(False)
            self.data_has_nan = False

    def fill_data(self):
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
            self.show_data()
            print(f'利用数据特征【{self.dataFillType.currentText()}】填充成功！')

    def select_output_dir_dialog(self, event):
        directory = QFileDialog.getExistingDirectory(self, 
                                                     "选择导出文件夹", 
                                                     self.cur_dir, 
                                                     QFileDialog.ShowDirsOnly | QFileDialog.DontResolveSymlinks)
        if directory:
            print(f"selected dir: {directory}")
            self.outputDirEdit.setText(directory)
            self.output_dir = directory
            
    def output_csv_file(self):
        if self.df_data is not None and \
                not self.data_has_nan and self.outputDirEdit.text():
            os.makedirs(self.output_dir, exist_ok=True)
            file_name = os.path.basename(self.input_path)
            file_name = os.path.splitext(file_name)[0] + '_filled.csv'
            output_path = os.path.join(self.output_dir, file_name)
            self.filled_df_data.to_csv(output_path, index=False)
            print(f'成功导出文件：{output_path}')

    def visualize(self):
        if self.df_data is not None and not self.data_has_nan:
            # print('可视化数据：')
            # print(self.filled_df_data)
            self.chart_window = ChartWindow(self.filled_df_data)
            self.chart_window.show()
        else:
            print('未导入CSV文件或数据存在缺失，无法可视化')

    def predict_new_data(self):
        if self.df_data is not None and not self.data_has_nan and self.predictNumEdit.text():
            n_predicts = int(self.predictNumEdit.text())
            new_df = pd.DataFrame()
            predictions = {}
            for col_name in self.filled_df_data.columns:
                col_df = self.filled_df_data[col_name]
                predictor = self.predictors[col_name]
                new_col_data = predictor.predict(n_predicts)
                predictions[col_name] = new_col_data.tolist()
                new_df[col_name] = pd.DataFrame(np.concatenate([col_df.values, new_col_data]))
            self.filled_df_data = new_df
            print(f'predictions:\n{predictions}')
            self.show_data()

    def __bind_all_functions(self):
        self.inputPathEdit.mousePressEvent = self.select_input_path_dialog
        self.outputDirEdit.mousePressEvent = self.select_output_dir_dialog
        self.visualizeBtn.clicked.connect(self.visualize)
        self.dataFillBtn.clicked.connect(self.fill_data)
        self.outputBtn.clicked.connect(self.output_csv_file)
        self.predictBtn.clicked.connect(self.predict_new_data)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
