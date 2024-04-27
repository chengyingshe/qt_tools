from enum import Enum
from typing import List
import pandas as pd

class ProcessType(Enum):
    AVERAGE = 1  # 平均数
    MEDIAN = 2  # 中位数
    MODE = 3  # 众数

class Preprocessor:
    """数据预处理类"""
    def process(self, df_data: pd.DataFrame, type: ProcessType):
        if type == ProcessType.AVERAGE:
            fill_val = df_data.mean()
        elif type == ProcessType.MEDIAN:
            fill_val = df_data.median()
        else:
            fill_val = df_data.mode()
        return df_data.fillna(fill_val)
    