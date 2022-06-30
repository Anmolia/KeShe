from pyecharts import options as opts
from pyecharts.charts import Kline,Bar,Line,Grid
import pandas as pd
from pyecharts.commons.utils import JsCode
import talib as ta
import numpy as np
# 财政收入
class E_C:
    def __init__(self):
        self.df = pd.read_csv(r"D:\Python3.9\Python_code\zonghekeshe\keshe1\files\gmjj\Enterprise_Confidence.csv",header=0)
    def processdata(self):
        print(self.df)
        print(self.df.columns)
        # self.df.replace({'Climate_Index_Enterprise':{"-",120},'Macro_econ_Climate_Index':{"-",120}},inplace=True)
        self.df.replace({'Climate_Index_Enterprise_YOY':{"-":'0.0%'},"Climate_Index_Enterprise_Comparative":{"-":'0.0%'},"Macro_econ_Climate_Index_YOY":{"-":'0.0%'},"Macro_econ_Climate_Index_Comparative":{"-":'0.0%'}},inplace=True)
        print(self.df.values)
        self.df = self.df.sort_values("Quarter",ascending=True)

    def display(self):
        x_data = self.df['Quarter'].values.tolist()
        y_data0 = [float(x.strip("%")) for x in self.df["Climate_Index_Enterprise_YOY"].values.tolist()]
        y_data1 = [float(x.strip("%")) for x in self.df["Climate_Index_Enterprise_Comparative"].values.tolist()]
        y_data2 = [float(x.strip("%")) for x in self.df["Macro_econ_Climate_Index_YOY"].values.tolist()]
        y_data3 = [float(x.strip("%")) for x in self.df["Macro_econ_Climate_Index_Comparative"].values.tolist()]
        line = (
            Line(init_opts=opts.InitOpts(width="1400px", height="600px"))
            .add_xaxis(
                xaxis_data=x_data
            )
            .add_yaxis(
                series_name="企业景气指数",
                y_axis=self.df['Climate_Index_Enterprise'].values.tolist(),
                linestyle_opts=opts.LineStyleOpts(width=2, opacity=1,color="#996600"),
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
                series_name="企业家信心指数",
                y_axis=self.df['Macro_econ_Climate_Index'].values.tolist(),
                linestyle_opts=opts.LineStyleOpts(width=2, opacity=1,color="#669966"),
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
            .add_yaxis(
                series_name="企业景气指数同比%",
                y_axis=y_data0,
                linestyle_opts=opts.LineStyleOpts(width=2, opacity=1,color="#006666"),
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
            .add_yaxis(
                series_name="企业景气指数环比%",
                y_axis=y_data1,
                linestyle_opts=opts.LineStyleOpts(width=2, opacity=1,color="#663399"),
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
            .add_yaxis(
                series_name="企业家信心指数同比%",
                y_axis=y_data2,
                linestyle_opts=opts.LineStyleOpts(width=2, opacity=1,color="#CC3399"),
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
            .add_yaxis(
                series_name="企业家信心指数环比%",
                y_axis=y_data3,
                linestyle_opts=opts.LineStyleOpts(width=2, opacity=1,color="#CC0000"),
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
                    # axislabel_opts=opts.LabelOpts(formatter="{value} %"),
                    axistick_opts=opts.AxisTickOpts(is_show=True),
                    splitline_opts=opts.SplitLineOpts(is_show=True),
                ),
                xaxis_opts=opts.AxisOpts(type_="category", boundary_gap=False),
                title_opts=opts.TitleOpts(title="中国企业情况"),
                datazoom_opts=[
                    opts.DataZoomOpts(
                        is_show=False, type_="inside", xaxis_index=[0, 0], range_start=98, range_end=100
                    ),
                ]
            )
            # .extend_axis(
            #     yaxis=opts.AxisOpts(
            #         # is_show=True,
            #         is_scale=True,
            #         axislabel_opts=opts.LabelOpts(formatter="{value}%"),
            #         axisline_opts = opts.AxisLineOpts(linestyle_opts=opts.LineStyleOpts(color='blue')),
            #         # axistick_opts=opts.AxisTickOpts(is_show=True),
            #         # splitline_opts=opts.SplitLineOpts(is_show=True),
            #         # min_ = 'dataMin'
            #     )
            # )  # 添加一条蓝色的y轴
            .render("中国企业景气及企业家信息情况.html")
        )

if __name__ == "__main__":
    a = E_C()
    a.processdata()
    a.display()