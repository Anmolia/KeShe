from pyecharts import options as opts
from pyecharts.charts import Kline,Bar,Line,Grid
import pandas as pd
from pyecharts.commons.utils import JsCode
import talib as ta

class stockallchart:
    def __init__(self):
        # 获取数据
        self.df = pd.read_csv(r"D:\Python3.9\Python_code\zonghekeshe\keshe1\files\stockall.csv", header=0)
        self.dates = list(self.df['date'])
    def drawKline(self):
        # print("时间", dates)
        # print("len：",len(dates))
        numdata = self.df[["open","high","low","close","volume"]].values.tolist()
        # print("数据：",numdata)
        # 绘制K线图
        c = (
            Kline()
            .add_xaxis(self.dates)
            .add_yaxis(
                "kline",
                numdata,
                markline_opts=opts.MarkLineOpts(
                    data=[opts.MarkLineItem(type_="max", value_dim="close")]
                ),
                itemstyle_opts=opts.ItemStyleOpts(  # 自定义颜色
                    color="#ef232a",
                    color0="#14b143",
                    border_color="#ef232a",
                    border_color0="#14b143",
                ),
            )
            .set_global_opts(
                xaxis_opts=opts.AxisOpts(is_scale=True),
                yaxis_opts=opts.AxisOpts(
                    is_scale=True,
                    splitarea_opts=opts.SplitAreaOpts(
                        is_show=True, areastyle_opts=opts.AreaStyleOpts(opacity=1)
                    ),
                ),
                # datazoom_opts=[ # opts.DataZoomOpts(pos_bottom="-2%")
                #                opts.DataZoomOpts(is_show=False, type_="inside", xaxis_index=[0, 0], range_end=100,pos_bottom="-2%"),
                #                # xaxis_i  ndex=[0, 0]设置第一幅图为内部缩放
                #                opts.DataZoomOpts(is_show=True, xaxis_index=[0, 1], pos_top="97%", range_end=100),
                #                # xaxis_index=[0, 1]连接第二幅图的axis
                #                opts.DataZoomOpts(is_show=False, xaxis_index=[0, 2], range_end=100),
                #                # xaxis_index=[0, 2]连接第三幅图的axis
                # ],
                datazoom_opts=[opts.DataZoomOpts(pos_bottom="-2%")],
                title_opts=opts.TitleOpts(title="股市趋势发展"),
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
                       y_axis=self.df['close'].rolling(10).mean(),
                       is_smooth=True,
                       linestyle_opts=opts.LineStyleOpts(opacity=1),
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
                title_opts=opts.TitleOpts(title="MA折线图"),
            )
        )
        print("MA获取成功！")
        return MALine
        # overlap_kline_ma = c.overlap(MALine)
        # return overlap_kline_ma
    def display(self):
        overlap_kline_ma = self.drawKline()
        print("kline1:",overlap_kline_ma)
        volumeFlag = self.df['close']-self.df['open']
        print(volumeFlag)
        # 最后的 Grid
        grid_chart = Grid(init_opts=opts.InitOpts(width="1400px", height="800px"))

        grid_chart.add_js_funcs(
            "var volumeFlag = {}".format(volumeFlag.values.tolist())
        )  # 传递涨跌数据给vomume绘图，用红色显示上涨成交量，绿色显示下跌成交量
        # K线图和 MA5 的折线图
        grid_chart.add(
            self.drawKline(),
            grid_opts=opts.GridOpts(pos_left="3%", pos_right="1%", height="60%"),
        )
        grid_chart.render("股市走向图.html")
if __name__ == "__main__":
    a = stockallchart()
    print(a.dates)
    a.display()