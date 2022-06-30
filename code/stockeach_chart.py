from pyecharts import options as opts
from pyecharts.charts import Kline,Bar,Line,Grid
import pandas as pd
from pyecharts.commons.utils import JsCode
import talib as ta
import numpy as np

class stockallchart:
    def __init__(self):
        # 获取数据
        self.df = pd.read_csv(r"D:\Python3.9\Python_code\zonghekeshe\keshe1\files\stockall_final.csv", header=0)
        self.dates = list(set(self.df['date']))
        self.groups = self.df.groupby('stock')
    def processdata(self,value):
        value['date'] = pd.to_datetime(value["date"])
        value['date'] = value['date'].apply(lambda x: x.strftime('%Y/%m/%d'))
        return value
    def drewKline(self):
        self.dates.sort()
        print(self.dates)
        c_0 = (
            Kline()
            .add_xaxis(xaxis_data=self.dates)
            .set_global_opts(
                xaxis_opts=opts.AxisOpts(
                    type_="category",
                        is_scale=True,
                        boundary_gap=False,
                        axisline_opts=opts.AxisLineOpts(is_on_zero=True),
                        splitline_opts=opts.SplitLineOpts(is_show=False),
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
                        is_show=True, xaxis_index=[0, 1], pos_top="98%", range_start=98, range_end=100
                    ),
                    opts.DataZoomOpts(is_show=False, xaxis_index=[0, 2], range_start=98, range_end=100),
                ],
                legend_opts=opts.LegendOpts(
                    is_show= True,
                    type_="scroll",
                    selected_mode="multiple",
                    pos_left="1%",
                    pos_top="3%",
                    item_gap=2,
                    orient="horizontal"
                ),
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
                title_opts=opts.TitleOpts(title="道琼斯工业指数走向", pos_left="0"),
            )
                    # .render("股票走势图1.html")
        )
        for key,value in self.groups:
            value = self.processdata(value)
            y_data = value[["open", "close", "low", "high", "volume"]].values.tolist()
            c = (
                Kline()
                .add_xaxis(xaxis_data=self.dates)
                .add_yaxis(
                    series_name=key,
                    y_axis=y_data,
                    itemstyle_opts=opts.ItemStyleOpts(  # 自定义颜色
                        color="#ef232a",
                        color0="#14b143",
                        border_color="#ef232a",
                        border_color0="#14b143",
                    ),
                    markline_opts=opts.MarkLineOpts(
                        data=[
                            opts.MarkLineItem(type_="max", value_dim="close"),
                            opts.MarkLineItem(type_='min', value_dim='close')
                        ],
                        precision=4,
                    ),
                )
            )
            MA = self.drawMAline(key,value)
            overlap_kline_line = c.overlap(MA)
            kline = c_0.overlap(overlap_kline_line)
        return kline
        # c_0.render("循环.html")
    def drawMAline(self,name,value):
        numdata = value[["open", "high", "low", "close", "volume"]].values.tolist()
        # print("数据：", numdata)
        MALine = (
            Line()
                .add_xaxis(self.dates)
                .add_yaxis(series_name=name+"_MA5",
                           y_axis=value['close'].rolling(5).mean(),
                           is_smooth=True,
                           linestyle_opts=opts.LineStyleOpts(opacity=1),#, color="#0066CC"),
                           label_opts=opts.LabelOpts(is_show=False),
                )
                .add_yaxis(
                series_name=name+"_MA10",
                y_axis=value['close'].rolling(10).mean(),
                is_smooth=True,
                linestyle_opts=opts.LineStyleOpts(opacity=1), #color="#FF6600"),
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
        print("MA获取成功！")
        return MALine

    def drawVolume(self):
        bar = (
            Bar()
            .add_xaxis(xaxis_data=self.dates)
            .set_global_opts(
                xaxis_opts=opts.AxisOpts(
                    type_="category",
                    is_scale=True,
                    grid_index=1,
                    boundary_gap=False,
                    axisline_opts=opts.AxisLineOpts(is_on_zero=False),
                    axistick_opts=opts.AxisTickOpts(is_show=False),
                    splitline_opts=opts.SplitLineOpts(is_show=False),
                    axislabel_opts=opts.LabelOpts(is_show=False),
                    split_number=20,
                    min_="dataMin",
                    max_="dataMax",
                ),
                yaxis_opts=opts.AxisOpts(
                    # name="volume",
                    grid_index=1,
                    is_scale=True,
                    split_number=2,
                    axislabel_opts=opts.LabelOpts(is_show=False),
                    axisline_opts=opts.AxisLineOpts(is_show=False),
                    axistick_opts=opts.AxisTickOpts(is_show=False),
                    splitline_opts=opts.SplitLineOpts(is_show=False),
                ),
                legend_opts=opts.LegendOpts(
                    is_show=True,
                    type_="scroll",
                    selected_mode="multiple",
                    pos_left="1%",
                    pos_top="65%",
                    item_gap=5,
                    orient="horizontal"
                ),
            )
        )
        for key,value in self.groups:
            volume = value['volume'].values.tolist()
            bar_1 = (
                Bar()
                .add_xaxis(xaxis_data=self.dates)
                .add_yaxis(
                    series_name=key+"_Volume",
                    y_axis=volume,
                    xaxis_index=1,
                    yaxis_index=1,
                    label_opts=opts.LabelOpts(is_show=False),
                )
            )
            vol_bar = bar.overlap(bar_1)
        return vol_bar
    def d_MACDS(self):
        bar_2 = (
            Bar()
            .add_xaxis(xaxis_data=self.dates)
            .set_global_opts(
                xaxis_opts=opts.AxisOpts(
                    type_="category",
                    grid_index=2,
                    axislabel_opts=opts.LabelOpts(is_show=False),
                ),
                yaxis_opts=opts.AxisOpts(
                    grid_index=2,
                    split_number=4,
                    axisline_opts=opts.AxisLineOpts(is_on_zero=False),
                    axistick_opts=opts.AxisTickOpts(is_show=False),
                    splitline_opts=opts.SplitLineOpts(is_show=False),
                    axislabel_opts=opts.LabelOpts(is_show=True),
                ),
                legend_opts=opts.LegendOpts(
                    is_show=True,
                    type_="scroll",
                    selected_mode="multiple",
                    pos_left="1%",
                    pos_top="80%",
                    item_gap=2,
                    orient="horizontal"
                ),
            )
        )
        for key,value in self.groups:
            value["DIFF"], value["DEA"], value["MACD"] = ta.MACD(value['close'].values)
            value["MACDS"] = value["MACD"] * 2
            value.replace(np.nan, 0, inplace=True)
            macds = value['MACDS'].values.tolist()
            bar_3 = (
                Bar()
                .add_xaxis(xaxis_data=self.dates)
                .add_yaxis(
                    series_name=key+"_MACD",
                    y_axis=macds,
                    xaxis_index=2,
                    yaxis_index=2,
                    label_opts=opts.LabelOpts(is_show=False),
                    itemstyle_opts=opts.ItemStyleOpts(
                        color=JsCode(
                            """
                                function(params) {
                                    var colorList;
                                    if (params.data >= 0) {
                                      colorList = '#ef232a';
                                    } else {
                                      colorList = '#14b143';
                                    }
                                    return colorList;
                                }
                                """
                        )
                    ),
                )
            )
            d_line = self.d_dline(key,value)
            overlap_bar_line = bar_3.overlap(d_line)
            bar_macd = bar_2.overlap(overlap_bar_line)

        return bar_macd
    def d_dline(self,name,value):
        lines = (
            Line()
            .add_xaxis(xaxis_data=self.dates)
            .add_yaxis(
                series_name=name+"_DIF",
                y_axis=value["DIFF"],
                xaxis_index=2,
                yaxis_index=2,
                label_opts=opts.LabelOpts(is_show=False),
                linestyle_opts=opts.LineStyleOpts(opacity=1, width=2)
            )
            .add_yaxis(
                series_name=name+"_DEA",
                y_axis=value["DEA"],
                xaxis_index=2,
                yaxis_index=2,
                label_opts=opts.LabelOpts(is_show=False),
                linestyle_opts=opts.LineStyleOpts(opacity=1, width=2),
            )
            .set_global_opts(legend_opts=opts.LegendOpts(is_show=False))
        )
        return lines

    def display(self):
        volumeFlag = self.df['close'] - self.df['open']
        print("变化量：", volumeFlag)
        # 最后的 Grid
        grid_chart = Grid(init_opts=opts.InitOpts(width="1500px", height="800px"))

        grid_chart.add_js_funcs(
            "var volumeFlag = {}".format(volumeFlag.values.tolist())
        )  # 传递涨跌数据给vomume绘图，用红色显示上涨成交量，绿色显示下跌成交量
        # K线图和 MA5 的折线图
        grid_chart.add(
            self.drewKline(),
            grid_opts=opts.GridOpts(
                pos_left="5%", pos_right="5%", height="53%"
            ),
        )
        grid_chart.add(
            self.drawVolume(),
            grid_opts=opts.GridOpts(
                pos_left="5%", pos_right="5%", pos_top="66%", height="12%"
            ),
        )
        grid_chart.add(
            self.d_MACDS(),
            grid_opts=opts.GridOpts(
                pos_left="5%", pos_right="5%", pos_top="84%", height="13%"
            ),
        )
        grid_chart.render("道琼斯工业指数单只走向.html")
if __name__ == "__main__":
    a = stockallchart()
    print(len(a.dates))
    print(len(a.groups))
    for key,value in a.groups:
        print("key:",key)
        print(value)
        print()
    a.display()