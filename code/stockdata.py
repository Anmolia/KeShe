import numpy as np

import pandas as pd

import talib as ta
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
        # print("行索引：",self.stockname)
        self.colname = self.df.columns
        # print("列索引：",self.colname)
        self.dates = list(set(self.df["date"]))
        self.dates.sort()
        # print("datas:", self.datas)
        # print("dates:",self.dates)
        print(len(self.dates))
    def fill_excel(self):
        print(self.df)
        groups = self.df.groupby("stock")
        # print("groups:",groups)
        for key, value in groups:
            # print("type:",type(key),"key:",key)
            if len(value.date) != 5284:
                a = list(set(self.dates) - set(value.date))
                a.sort()
                i = 0
                for each in a:
                    self.df = self.df.append({"stock": key, "date": each, "open": 0, "high": 0, "low": 0, "close": 0,
                                              "adj_close": 0, "volume": 0, "dividend": 0, "split": 1},
                                             ignore_index=True)
                    print(i)
                    i += 1
                # print(key,a)
            else:
                print(key)
        self.df.sort_index()
        print("self.df", self.df)
        self.df.to_csv(r"D:\Python3.9\Python_code\zonghekeshe\keshe1\files\stockall_final.csv")
    # 获取每个日期的股票的总值
    def getdate_sum(self):
        print(self.df)
        groups = self.df.groupby('date').agg("sum")
        print("groups:",groups)
        print(len(groups))
        print("type:",type(groups))
        print("行索引：",groups.index)
        print("列索引：",groups.columns)
        groups.to_csv(r"D:\Python3.9\Python_code\zonghekeshe\keshe1\files\stockall.csv")
    def getdate_ave(self):

        groups = self.df.groupby('date').agg("mean")
        # y_value = [int(y) for y in groups['volume'].values]
        # print("成交量：", y_value)
        # groups['volume'] = y_value
        groups["DIFF"], groups["DEA"], groups["MACD"] = ta.MACD(groups['close'].values)
        groups["MACDS"] = groups["MACD"] * 2
        groups.replace(np.nan, 0, inplace=True)
        # y_value1 = [y*100 for y in groups["DIFF"]]
        # groups["DIFF"] = y_value1
        # y_value2 = [y*100 for y in groups["DEA"]]
        # groups["DEA"] = y_value2
        # print("MACD:", groups["MACDS"])
        # y_value3 = [int(y*100) for y in groups["MACDS"].values]
        # print("MACDS取整",y_value3)
        # groups['MACDS'] = y_value3

        print(groups)
        groups.to_csv(r"D:\Python3.9\Python_code\zonghekeshe\keshe1\files\stockall_ave.csv")
    def getall_ave(self):
        groups = self.df.groupby('stock').agg("mean")
        print("groups:", groups)
        print(len(groups))
        groups.to_csv(r"D:\Python3.9\Python_code\zonghekeshe\keshe1\files\stockave.csv")
    def data_run(self):
        self.class_index_data()
        l = list(self.df.split)
        print(len(l))
        self.fill_excel()
        self.getdate_sum()
        self.getdate_ave()
        self.getall_ave()
        l = list(self.df.split)
        print(len(l))

if __name__ == "__main__":
    a = stockprocess()
    # a.class_index_data()
    # a.getall_data()
    # a.getall_ave()
    a.data_run()