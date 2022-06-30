from pyecharts import options as opts
from pyecharts.charts import Kline,Bar,Line,Grid
import pandas as pd
from pyecharts.commons.utils import JsCode
import talib as ta
import numpy as np
# 财政收入
class china_FR:
    def __init__(self):
        self.df = pd.read_csv(r"D:\Python3.9\Python_code\zonghekeshe\keshe1\files\gmjj\Fiscal_Revenue.csv",header=0)
    def processdata(self):
        print(self.df)
        print(self.df.columns)
        self.df = self.df.sort_values("Month",ascending=True)
        # self.df = self.df.reindex(index=range(0,165))
        print(self.df)
    def draw_line1(self):
        numdata = self.df[['Month', 'Current_Month_Value', 'Total']]
        x_data = numdata['Month'].values.tolist()
        # print(x_data)
        line1 = (
            Line(init_opts=opts.InitOpts(width="1500px",height="600px"))
            .add_xaxis(
                xaxis_data=x_data
            )
            .add_yaxis(
                series_name="当月收入(亿元)",
                y_axis=numdata['Current_Month_Value'].values.tolist(),
                linestyle_opts=opts.LineStyleOpts(width=2,opacity=1, color="#FF6600"),
                label_opts=opts.LabelOpts(is_show=False),
                markpoint_opts=opts.MarkPointOpts(
                    data=[
                        opts.MarkPointItem(type_="max", name="最大值",symbol_size=80),
                        opts.MarkPointItem(type_="min", name="最小值",symbol_size=80),
                    ]
                ),
                markline_opts=opts.MarkLineOpts(data=[opts.MarkLineItem(type_="average")])

            )
            .add_yaxis(
                series_name="总计收入(亿元)",
                y_axis=numdata['Total'].values.tolist(),
                linestyle_opts=opts.LineStyleOpts(width=2,opacity=1, color="#0066CC"),
                label_opts=opts.LabelOpts(is_show=False),
                markpoint_opts=opts.MarkPointOpts(
                    data=[
                        opts.MarkPointItem(type_="max", name="平均值",symbol_size=80),
                        opts.MarkPointItem(type_="min", name="最小值",symbol_size=80),
                    ]
                ),
                markline_opts=opts.MarkLineOpts(data=[opts.MarkLineItem(type_="average")]),
            )
            .set_global_opts(
                tooltip_opts=opts.TooltipOpts(trigger="axis"),
                yaxis_opts=opts.AxisOpts(
                    type_="value",
                    axistick_opts=opts.AxisTickOpts(is_show=True),
                    splitline_opts=opts.SplitLineOpts(is_show=True),
                ),
                xaxis_opts=opts.AxisOpts(type_="category", boundary_gap=False),
                title_opts=opts.TitleOpts(title="中国财政收入"),
                datazoom_opts=[
                    opts.DataZoomOpts(
                        is_show=False, type_="inside", pos_bottom="2%", xaxis_index=[0, 0], range_start=98, range_end=100
                    ),
                ]
            )
            .render("中国财政收入.html")
        )
        # return line1
    def draw_line2(self):
        numdata = self.df[['Month', 'Current_Month_YOY', 'Current_Month_Comparattive', 'Total_YOY']]
        x_data = numdata['Month'].values.tolist()
        y_data1 = [float(x.strip("%")) for x in numdata["Current_Month_YOY"].values.tolist()]
        y_data2 = [float(x.strip("%")) for x in numdata["Current_Month_Comparattive"].values.tolist()]
        y_data3 = [float(x.strip("%")) for x in numdata["Total_YOY"].values.tolist()]
        line2 = (
            Line(init_opts=opts.InitOpts(width="1500px",height="600px"))
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
                # markline_opts=opts.MarkLineOpts(
                #     data=[opts.MarkLineItem(type_="average")],
                #     label_opts=opts.LabelOpts(
                #         font_size=15,margin=50)
                # )

            )
            .add_yaxis(
                series_name="当月环比增长",
                y_axis=y_data2,
                linestyle_opts=opts.LineStyleOpts(width=2, opacity=1),
                label_opts=opts.LabelOpts(is_show=False),
                markpoint_opts=opts.MarkPointOpts(
                    data=[
                        opts.MarkPointItem(type_="max", name="平均值", symbol_size=45),
                        opts.MarkPointItem(type_="min", name="最小值", symbol_size=45),
                    ]
                ),
                # markline_opts=opts.MarkLineOpts(
                #     data=[opts.MarkLineItem(type_="average")],
                #     label_opts=opts.LabelOpts(font_size=15)
                # ),
            )
            .add_yaxis(
                series_name="累计同比增长",
                y_axis=y_data3,
                linestyle_opts=opts.LineStyleOpts(width=2, opacity=1),
                label_opts=opts.LabelOpts(is_show=False),
                markpoint_opts=opts.MarkPointOpts(
                    data=[
                        opts.MarkPointItem(type_="max", name="平均值", symbol_size=45),
                        opts.MarkPointItem(type_="min", name="最小值", symbol_size=45),
                    ]
                ),
                # markline_opts=opts.MarkLineOpts(
                #     data=[
                #         opts.MarkLineItem(type_="average"),
                #     ],
                #     label_opts=opts.LabelOpts(font_size=15)
                # ),
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
                title_opts=opts.TitleOpts(title="中国财政收入增长率"),
                datazoom_opts=[
                    opts.DataZoomOpts(
                        is_show=False, type_="inside", xaxis_index=[0, 0], range_start=98, range_end=100
                    ),
                ]
            )
                .render("中国财政收入增长率.html")
        )
    def display(self):
        self.processdata()
        self.draw_line1()
        self.draw_line2()

if __name__ == "__main__":
    a = china_FR()
    a.display()