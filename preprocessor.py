import pandas as pd

class Preprocessor:
    """数据预处理类"""
    def __init__(self, df_data: pd.DataFrame):
        self.data = df_data  # 处理前的数据
        self.processed_data = None  # 处理后的数据

    def process_col(self, col_name, type) -> None:
        """处理单列数据：填充缺失值
        
        Keyword arguments:
        col_name -- 指定列名
        type -- 处理方式
        Return: None（需要对processed_data进行修改）
        """
        
        pass