from pyecharts import options as opts
from pyecharts.charts import Kline,Bar,Line,Grid
import pandas as pd

class stockprocess:
    def __init__(self):
        # 获取数据
        self.df = pd.read_csv(r"D:\Python3.9\Python_code\zonghekeshe\keshe1\files\dow_historic_2000_2020.csv",header = 0)
        self.colname = []   # 列名
        self.stockname = [] # 股票名
        self.datas = pd.DataFrame()
        self.alldata = {}
        self.dates = []
    def class_index_data(self):
        # print(self.df.dtypes)
        self.stockname = list(set(self.df.stock))
        self.stockname.sort()
        print("行索引：",self.stockname)
        self.colname = self.df.columns
        print("列索引：",self.colname)
        self.dates = list(set(self.df["date"]))
        self.dates.sort()
        # print("datas:", self.datas)
        print("dates:",self.dates)
        print(len(self.dates))
    # 获取每个日期的股票的总值
    def getall_data(self):
        groups = self.df.groupby('date').agg("sum")
        print("groups:",groups)
        print(len(groups))
        print("type:",type(groups))
        print("行索引：",groups.index)
        print("列索引：",groups.columns)
        groups.to_csv(r"D:\Python3.9\Python_code\zonghekeshe\keshe1\files\stockall.csv")
    def getall_ave(self):
        groups = self.df.groupby('stock').agg("mean")
        print("groups:", groups)
        print(len(groups))
        groups.to_csv(r"D:\Python3.9\Python_code\zonghekeshe\keshe1\files\stockave.csv")
    def data_run(self):
        self.class_index_data()
        self.getall_data()
        self.getall_ave()
if __name__ == "__main__":
    a = stockprocess()
    # a.class_index_data()
    # a.getall_data()
    # a.getall_ave()
    a.data_run()