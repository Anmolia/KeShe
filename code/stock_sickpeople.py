import time

from pyecharts import options as opts
from pyecharts.charts import Kline,Bar,Line,Grid
import pandas as pd
from pyecharts.commons.utils import JsCode
import talib as ta
import numpy as np

class stock_people:
    def __init__(self):
        self.dfstock = pd.read_csv(r"D:\Python3.9\Python_code\zonghekeshe\keshe1\files\stockall_ave.csv", header=0)
        self.dfpeople = pd.read_csv(r"D:\Python3.9\Python_code\zonghekeshe\keshe1\files\owid-covid-data.csv", header=0)
        self.data = pd.DataFrame()
    def processdata(self):
        # print(self.dfstock['date'])
        data1 = self.dfpeople[['date','total_cases']]
        # print(data1)
        # print("self.dfpeople['date']",self.dfpeople['date'])
        # print("self.dfpeople['total_cases']",self.dfpeople['total_cases'])
        data2 = self.dfstock[(self.dfstock["date"]>="2020/2/24")]
        print(type(data2))
        data3 = data1[(data1["date"]>="2020-02-24")&(data1['date']<="2020-09-09")]
        print("data3",data3)
        # print(type(data3))
        data2['date'] = pd.to_datetime(data2["date"])
        data2['date'] = data2['date'].apply(lambda x: x.strftime('%Y/%m/%d'))

        data3['date'] = pd.to_datetime(data3["date"])
        data3['date'] = data3['date'].apply(lambda x: x.strftime('%Y/%m/%d'))
        # data2.date.head()
        print(data2)
        data3 = data3.groupby('date').agg("sum")
        print(data3)
        self.data = pd.merge(data2,data3,on="date")
        self.data.replace(np.nan, 0, inplace=True)
        # self.data.to_csv(r"D:\Python3.9\Python_code\zonghekeshe\keshe1\files\test.csv")
        print(self.data)
    def drawKline(self):
        numdata = self.data[["open", "close", "low", "high", "volume"]].values.tolist()
        # 绘制K线图
        date = self.data['date'].values.tolist()
        print(date)
        print("date",date)
        c = (
            Kline()
            .add_xaxis(xaxis_data=date)
            .add_yaxis(
                "kline",
                y_axis=numdata,
                itemstyle_opts=opts.ItemStyleOpts(  # 自定义颜色
                    color="#ec0000",
                    color0="#00da3c"
                ),
                markline_opts=opts.MarkLineOpts(
                    data=[
                        opts.MarkLineItem(type_="max", value_dim="close"),
                        opts.MarkLineItem(type_='min', value_dim='close')
                    ],
                    precision=4,
                ),
            )
            .set_global_opts(
                xaxis_opts=opts.AxisOpts(
                    type_="category",
                    is_scale=True,
                    boundary_gap=False,
                    axisline_opts=opts.AxisLineOpts(is_on_zero=True),
                    splitline_opts=opts.SplitLineOpts(is_show=False),
                    # split_number=20,
                    min_="dataMin",
                    max_="dataMax",
                ),
                yaxis_opts=opts.AxisOpts(
                    is_scale=True, splitline_opts=opts.SplitLineOpts(is_show=True)
                ),
                tooltip_opts=opts.TooltipOpts(
                    trigger="axis",
                    axis_pointer_type="cross",
                    background_color="rgba(245, 245, 245, 0.8)",
                    border_width=1,
                    border_color="#ccc",
                    textstyle_opts=opts.TextStyleOpts(color="#000"),
                ),
                datazoom_opts=[
                    opts.DataZoomOpts(
                        is_show=False, type_="inside", xaxis_index=[0, 0], range_start=98, range_end=100
                    ),
                    opts.DataZoomOpts(
                        is_show=True, xaxis_index=[0, 1], pos_top="99%", range_start=98, range_end=100
                    ),
                ],
                visualmap_opts=opts.VisualMapOpts(
                    is_show=False,
                    dimension=2,
                    series_index=5,
                    is_piecewise=True,
                    pieces=[
                        {"value": 1, "color": "#00da3c"},
                        {"value": -1, "color": "#ec0000"},
                    ],
                ),
                axispointer_opts=opts.AxisPointerOpts(
                    is_show=True,
                    link=[{"xAxisIndex": "all"}],
                    label=opts.LabelOpts(background_color="#777"),
                ),
                title_opts=opts.TitleOpts(title="新冠肺炎疫情期间道琼斯工业指数", pos_left="0"),
                brush_opts=opts.BrushOpts(
                    x_axis_index="all",
                    brush_link="all",
                    out_of_brush={"colorAlpha": 0.1},
                    brush_type="lineX",
                ),
            )
            # .render("股票走势图1.html")
        )
        MA = self.draw_Maline()
        overlap_kline_ma = c.overlap(MA)
        return overlap_kline_ma
    def draw_Maline(self):
        numdata = self.data[["open", "close", "low", "high", "volume"]].values.tolist()
        # 绘制K线图
        date = self.data['date'].values.tolist()
        MALine = (
            Line()
            .add_xaxis(date)
            .add_yaxis(series_name="MA5",
                           y_axis=self.data['close'].rolling(5).mean(),
                           is_smooth=True,
                           linestyle_opts=opts.LineStyleOpts(opacity=1, color="#0066CC"),
                           label_opts=opts.LabelOpts(is_show=False),
                           )
            .add_yaxis(
                series_name="MA10",
                y_axis=self.data['close'].rolling(10).mean(),
                is_smooth=True,
                linestyle_opts=opts.LineStyleOpts(opacity=1, color="#FF6600"),
                label_opts=opts.LabelOpts(is_show=False),
            )
            .set_global_opts(
                xaxis_opts=opts.AxisOpts(
                    type_='category',
                    grid_index=1,
                    axislabel_opts=opts.LabelOpts(is_show=False)
                ),
                yaxis_opts=opts.AxisOpts(
                    grid_index=1,
                    split_number=3,
                    axisline_opts=opts.AxisLineOpts(is_on_zero=False),
                    axistick_opts=opts.AxisTickOpts(is_show=False),
                    splitline_opts=opts.SplitLineOpts(is_show=False),
                    axislabel_opts=opts.LabelOpts(is_show=True),
                ),
                # title_opts=opts.TitleOpts(title="MA折线图"),
            )
        )
        print("MA获取成功!")
        return MALine
    def draw_sickedpeople(self):
        total = self.data["total_cases"].values.tolist()
        date = self.data['date'].values.tolist()
        bar=(
            Bar()
            .add_xaxis(xaxis_data=date)
            .add_yaxis(
                series_name="Diagnosed",
                y_axis=total,
                xaxis_index=1,
                yaxis_index=1,
                label_opts=opts.LabelOpts(is_show=False),
            )
            .set_global_opts(
                xaxis_opts=opts.AxisOpts(
                    type_="category",
                    is_scale=True,
                    grid_index=1,
                    is_show=True,
                    boundary_gap=False,
                    axisline_opts=opts.AxisLineOpts(is_on_zero=False),
                    axistick_opts=opts.AxisTickOpts(is_show=False),
                    splitline_opts=opts.SplitLineOpts(is_show=True),
                    axislabel_opts=opts.LabelOpts(is_show=False),
                    split_number=20,
                    min_="dataMin",
                    max_="dataMax",
                ),
                yaxis_opts=opts.AxisOpts(
                    # name="volume",
                    # type_="catagory",
                    is_show=True,
                    grid_index=1,
                    is_scale=True,
                    split_number=2,
                    axislabel_opts=opts.LabelOpts(is_show=True),
                    axisline_opts=opts.AxisLineOpts(is_show=True),
                    axistick_opts=opts.AxisTickOpts(is_show=False),
                    splitline_opts=opts.SplitLineOpts(is_show=True),
                ),
                legend_opts=opts.LegendOpts(is_show=False),
            )
        )
        return bar
    def display(self):
        volumeFlag = self.data['close'] - self.data['open']
        grid_chart = Grid(init_opts=opts.InitOpts(width="1500px", height="800px"))
        grid_chart.add_js_funcs(
            "var volumeFlag = {}".format(volumeFlag.values.tolist())
        )  # 传递涨跌数据给vomume绘图，用红色显示上涨成交量，绿色显示下跌成交量
        # K线图和 MA5 的折线图
        grid_chart.add(
            self.drawKline(),
            grid_opts=opts.GridOpts(
                pos_left="5%", pos_right="5%", height="50%"
            ),
        )
        grid_chart.add(
            self.draw_sickedpeople(),
            grid_opts=opts.GridOpts(
                pos_left="5%", pos_right="5%", pos_top="61%", height="20%"
            ),
        )
        grid_chart.render("确诊人数和经济走向.html")

if __name__ == "__main__":
    a = stock_people()
    a.processdata()
    a.display()