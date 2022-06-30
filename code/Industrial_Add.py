from pyecharts import options as opts
from pyecharts.charts import Kline,Bar,Line,Grid
import pandas as pd
from pyecharts.commons.utils import JsCode
import talib as ta
import numpy as np
# 财政收入
class Industrial_Add:
    def __init__(self):
        self.df = pd.read_csv(r"D:\Python3.9\Python_code\zonghekeshe\keshe1\files\gmjj\Industrial_Added_Value.csv",header=0)
    def processdata(self):
        print(self.df)
        print(self.df.columns)
        self.df = self.df.sort_values("Month",ascending=True)
        # self.df = self.df.reindex(index=range(0,165))
        print(self.df)
    def display(self):
        x_data = self.df['Month'].values.tolist()
        y_data1 = [float(x.strip("%")) for x in self.df["YOY"].values.tolist()]
        y_data2 = [float(x.strip("%")) for x in self.df["Cumulative_Growth"].values.tolist()]
        line2 = (
            Line(init_opts=opts.InitOpts(width="1500px", height="600px"))
            .add_xaxis(
                xaxis_data=x_data
            )
            .add_yaxis(
                series_name="当月同比增长",
                y_axis=y_data1,
                linestyle_opts=opts.LineStyleOpts(width=2, opacity=1),
                label_opts=opts.LabelOpts(is_show=False),
                markpoint_opts=opts.MarkPointOpts(
                    data=[
                        opts.MarkPointItem(type_="max", name="最大值", symbol_size=45),
                        opts.MarkPointItem(type_="min", name="最小值", symbol_size=45),
                    ]
                ),
                markline_opts=opts.MarkLineOpts(
                    data=[opts.MarkLineItem(type_="average")],
                    label_opts=opts.LabelOpts(
                        font_size=15)
                )

            )
            .add_yaxis(
                series_name="累计增长",
                y_axis=y_data2,
                linestyle_opts=opts.LineStyleOpts(width=2, opacity=1),
                label_opts=opts.LabelOpts(is_show=False),
                markpoint_opts=opts.MarkPointOpts(
                    data=[
                        opts.MarkPointItem(type_="max", name="平均值", symbol_size=45),
                        opts.MarkPointItem(type_="min", name="最小值", symbol_size=45),
                    ]
                ),
                markline_opts=opts.MarkLineOpts(
                    data=[
                        opts.MarkLineItem(type_="average"),
                    ],
                    label_opts=opts.LabelOpts(font_size=15)
                ),

            )
            .set_global_opts(
                tooltip_opts=opts.TooltipOpts(trigger="axis"),
                yaxis_opts=opts.AxisOpts(
                    type_="value",
                    axislabel_opts=opts.LabelOpts(formatter="{value} %"),
                    axistick_opts=opts.AxisTickOpts(is_show=True),
                    splitline_opts=opts.SplitLineOpts(is_show=True),
                ),
                xaxis_opts=opts.AxisOpts(type_="category", boundary_gap=False),
                title_opts=opts.TitleOpts(title="中国工业值增长率"),
                datazoom_opts=[
                    opts.DataZoomOpts(
                        is_show=False, type_="inside", xaxis_index=[0, 0], range_start=98, range_end=100
                    ),
                ]
            )
            .render("中国工业增加率.html")
        )
if __name__ == "__main__":
    a = Industrial_Add()
    a.processdata()
    a.display()