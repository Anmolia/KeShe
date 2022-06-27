from pyecharts import options as opts
from pyecharts.charts import Kline,Bar,Line,Grid
import pandas as pd
from pyecharts.commons.utils import JsCode
import talib as ta

class stockallchart:
    def __init__(self):
        # 获取数据
        self.df = pd.read_csv(r"D:\Python3.9\Python_code\zonghekeshe\keshe1\files\stockall_ave.csv", header=0)
        self.dates = list(self.df['date'])
    def drawKline(self):
        # print("时间", dates)
        # print("len：",len(dates))
        numdata = self.df[["open","close","low","high","volume"]].values.tolist()
        # print("数据：",numdata)
        # 绘制K线图
        c = (
            Kline()
            .add_xaxis(xaxis_data=self.dates)
            .add_yaxis(
                "kline",
                y_axis=numdata,
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
                        is_show=False, type_="inside", xaxis_index=[0, 0],range_start=98, range_end=100
                    ),
                    opts.DataZoomOpts(
                        is_show=True, xaxis_index=[0, 1], pos_top="99%",range_start=98, range_end=100
                    ),
                    opts.DataZoomOpts(is_show=False, xaxis_index=[0, 2],range_start=98, range_end=100),
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
                title_opts=opts.TitleOpts(title="道琼斯工业指数平均走向",pos_left="0"),
                brush_opts=opts.BrushOpts(
                    x_axis_index="all",
                    brush_link="all",
                    out_of_brush={"colorAlpha": 0.1},
                    brush_type="lineX",
                ),
            )
            # .render("股票走势图1.html")
        )
        # 绘制MA图
        line1 = self.MA_5_drawer()
        overlap_kline_ma = c.overlap(line1)
        return overlap_kline_ma

    def MA_5_drawer(self):
        # print("时间", dates)
        numdata = self.df[["open", "high", "low", "close", "volume"]].values.tolist()
        # print("数据：", numdata)
        MALine = (
            Line()
            .add_xaxis(self.dates)
            .add_yaxis(series_name="MA5",
                       y_axis=self.df['close'].rolling(5).mean(),
                       is_smooth=True,
                       linestyle_opts=opts.LineStyleOpts(opacity=1,color="#0066CC"),
                       label_opts=opts.LabelOpts(is_show=False),
            )
            .add_yaxis(
                series_name="MA10",
                y_axis=self.df['close'].rolling(10).mean(),
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
        print("MA获取成功！")
        return MALine
        # overlap_kline_ma = c.overlap(MALine)
        # return overlap_kline_ma

    def getvolumn(self):
        # volumeFlag = self.df['close'] - self.df['open']
        print("成交量",self.df['volume'])
        print(self.df['volume'])
        volume = self.df['volume'].values.tolist()
        bar_1 = (
            Bar()
            .add_xaxis(xaxis_data=self.dates)
            .add_yaxis(
                series_name="Volume",
                y_axis=volume,
                xaxis_index=1,
                yaxis_index=1,
                label_opts=opts.LabelOpts(is_show=False),
            )
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
                legend_opts=opts.LegendOpts(is_show=False),
            )
        )
        return bar_1
    def getMADC(self):
        # 获取MADC指标
        macds = self.df['MACDS'].values.tolist()
        bar_2 = (
            Bar()
            .add_xaxis(xaxis_data=self.dates)
            .add_yaxis(
                series_name="MACD",
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
                legend_opts=opts.LegendOpts(is_show=False),
            )
        )
        lines = (
            Line()
            .add_xaxis(xaxis_data=self.dates)
            .add_yaxis(
                series_name="DIF",
                y_axis=self.df["DIFF"],
                xaxis_index=2,
                yaxis_index=2,
                label_opts=opts.LabelOpts(is_show=False),
                linestyle_opts=opts.LineStyleOpts(opacity=1,width=2)
            )
            .add_yaxis(
                series_name="DEA",
                y_axis=self.df["DEA"],
                xaxis_index=2,
                yaxis_index=2,
                label_opts=opts.LabelOpts(is_show=False),
                linestyle_opts=opts.LineStyleOpts(opacity=1, width=2),
            )
            .set_global_opts(legend_opts=opts.LegendOpts(is_show=False))
        )
        overlap_bar_line = bar_2.overlap(lines)
        return overlap_bar_line

    def display(self):
        # overlap_kline_ma = self.drawKline()
        # print("kline1:",overlap_kline_ma)
        # bars = self.getvolumn()
        # print("成交量：",bars)
        volumeFlag = self.df['close']-self.df['open']
        print("变化量：",volumeFlag)
        # 最后的 Grid
        grid_chart = Grid(init_opts=opts.InitOpts(width="1500px", height="800px"))

        grid_chart.add_js_funcs(
            "var volumeFlag = {}".format(volumeFlag.values.tolist())
        )  # 传递涨跌数据给vomume绘图，用红色显示上涨成交量，绿色显示下跌成交量
        # K线图和 MA5 的折线图
        grid_chart.add(
            self.drawKline(),
            grid_opts=opts.GridOpts(
                pos_left="3%", pos_right="5%", height="60%"
            ),
        )
        grid_chart.add(
            self.getvolumn(),
            grid_opts=opts.GridOpts(
                pos_left="3%", pos_right="5%", pos_top="71%", height="10%"
            ),
        )
        grid_chart.add(
            self.getMADC(),
            grid_opts=opts.GridOpts(
                pos_left="3%", pos_right="5%", pos_top="83%", height="14%"
            ),
        )
        grid_chart.render("道琼斯工业指数平均走向.html")

    # def test(self):
    #     self.getvolandline()
if __name__ == "__main__":
    a = stockallchart()
    print(len(a.dates))
    a.display()
    print(a.df.columns)
    # a.test()