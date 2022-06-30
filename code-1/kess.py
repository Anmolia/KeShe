import json
from pyecharts.charts import Line, Page, Bar, Timeline, Pie
from wordcloud import WordCloud
import os
import jieba.analyse
import matplotlib.pyplot as plt
import sklearn
import numpy as np
import pandas as pd
from pyecharts.charts import Map
from pyecharts import options as opts
stopw=['以上','浏览器','9.0','做好','之','内蒙古自治区人民政府','吉林省人民政府','非必要','IE','Fujian','Provincial']
class covid():
    def __init__(self):
        self.l1=[]
        self.l2=[]
        self.cont=[]
        self.zhou={}
        self.cun=['Somalia', 'Liechtenstein', 'Morocco', 'W. Sahara', 'Serbia', 'Afghanistan', 'Angola', 'Albania', 'Andorra', 'United Arab Emirates', 'Argentina', 'Armenia', 'Australia', 'Austria', 'Azerbaijan', 'Burundi', 'Belgium', 'Benin', 'Burkina Faso', 'Bangladesh', 'Bulgaria', 'Bahrain', 'Bahamas', 'Bosnia and Herz.', 'Belarus', 'Belize', 'Bermuda', 'Bolivia', 'Brazil', 'Barbados', 'Brunei', 'Bhutan', 'Botswana', 'Central African Rep.', 'Canada', 'Switzerland', 'Chile', 'China', "Côte d'Ivoire", 'Cameroon', 'Dem. Rep. Congo', 'Congo', 'Colombia', 'Cape Verde', 'Costa Rica', 'Cuba', 'N. Cyprus', 'Cyprus', 'Czech Rep.', 'Germany', 'Djibouti', 'Denmark', 'Dominican Rep.', 'Algeria', 'Ecuador', 'Egypt', 'Eritrea', 'Spain', 'Estonia', 'Ethiopia', 'Finland', 'Fiji', 'France', 'Gabon', 'United Kingdom', 'Georgia', 'Ghana', 'Guinea', 'Gambia', 'Guinea-Bissau', 'Eq. Guinea', 'Greece', 'Grenada', 'Greenland', 'Guatemala', 'Guam', 'Guyana', 'Honduras', 'Croatia', 'Haiti', 'Hungary', 'Indonesia', 'India', 'Br. Indian Ocean Ter.', 'Ireland', 'Iran', 'Iraq', 'Iceland', 'Israel', 'Italy', 'Jamaica', 'Jordan', 'Japan', 'Siachen Glacier', 'Kazakhstan', 'Kenya', 'Kyrgyzstan', 'Cambodia', 'Korea', 'Kuwait', 'Lao PDR', 'Lebanon', 'Liberia', 'Libya', 'Sri Lanka', 'Lesotho', 'Lithuania', 'Luxembourg', 'Latvia', 'Moldova', 'Madagascar', 'Mexico', 'Macedonia', 'Mali', 'Malta', 'Myanmar', 'Montenegro', 'Mongolia', 'Mozambique', 'Mauritania', 'Mauritius', 'Malawi', 'Malaysia', 'Namibia', 'New Caledonia', 'Niger', 'Nigeria', 'Nicaragua', 'Netherlands', 'Norway', 'Nepal', 'New Zealand', 'Oman', 'Pakistan', 'Panama', 'Peru', 'Philippines', 'Papua New Guinea', 'Poland', 'Puerto Rico', 'Dem. Rep. Korea', 'Portugal', 'Paraguay', 'Palestine', 'Qatar', 'Romania', 'Russia', 'Rwanda', 'Saudi Arabia', 'Sudan', 'S. Sudan', 'Senegal', 'Singapore', 'Solomon Is.', 'Sierra Leone', 'El Salvador', 'Suriname', 'Slovakia', 'Slovenia', 'Sweden', 'Swaziland', 'Seychelles', 'Syria', 'Chad', 'Togo', 'Thailand', 'Tajikistan', 'Turkmenistan', 'Timor-Leste', 'Tonga', 'Trinidad and Tobago', 'Tunisia', 'Turkey', 'Tanzania', 'Uganda', 'Ukraine', 'Uruguay', 'United States', 'Uzbekistan', 'Venezuela', 'Vietnam', 'Vanuatu', 'Yemen', 'South Africa', 'Zambia', 'Zimbabwe', 'Aland', 'American Samoa', 'Fr. S. Antarctic Lands', 'Antigua and Barb.', 'Comoros', 'Curaçao', 'Cayman Is.', 'Dominica', 'Falkland Is.', 'Faeroe Is.', 'Micronesia', 'Heard I. and McDonald Is.', 'Isle of Man', 'Jersey', 'Kiribati', 'Saint Lucia', 'N. Mariana Is.', 'Montserrat', 'Niue', 'Palau', 'Fr. Polynesia', 'S. Geo. and S. Sandw. Is.', 'Saint Helena', 'St. Pierre and Miquelon', 'São Tomé and Principe', 'Turks and Caicos Is.', 'St. Vin. and Gren.', 'U.S. Virgin Is.', 'Samoa']
        self.month = ['2020-01-31', '2020-02-29', '2020-03-31', '2020-04-30', '2020-05-31', '2020-06-30', '2020-07-31',
                      '2020-08-31', '2020-09-30',
                      '2020-10-31', '2020-11-30', '2020-12-31',
                      '2021-01-31', '2021-02-28', '2021-03-31', '2021-04-30', '2021-05-31', '2021-06-30', '2021-07-31',
                      '2021-08-31',
                      '2021-09-30', '2021-10-31', '2021-11-30', '2021-12-31', '2022-01-31', '2022-02-28', '2022-03-11'
                      ]
        self.line_map()
    def openf(self,path):
        l = []
        for root,dir,files in os.walk(path):
            for file in files:
                l.append(os.path.join(root,file))
        for i in l:
            try:
                df=pd.read_csv(i)
                print(df[:5])
            except:
                print('error')
    def openw(self):
        path='E:\学习\课程设计三\owid-covid-data.csv'
        df = pd.read_csv(path,index_col=0)
        # l=df.loc[:,['location','date','total_cases','total_vaccinations','total_deaths']]
        l = df.loc[:, ['location', 'date', 'total_cases', 'total_vaccinations', 'total_deaths', 'people_vaccinated',
                       'total_boosters', 'total_vaccinations_per_hundred', 'people_vaccinated_per_hundred','total_boosters_per_hundred']]
        l2=df.loc[:,['date','location','total_cases','total_deaths']]
        l = l.fillna(0)
        l.replace(np.nan, 0,inplace=True)
        group = l.groupby("location")
        self.cont=list(group)
        dataa= np.array(l)
        self.l1=dataa.tolist()
        dat1 = np.array(l2)
        self.l2 = dat1.tolist()
    def line_map(self):
        self.openw()
        dict={}
        dict2={}
        world=[]
        china=[]
        for i in self.cont:
            list1=np.array(i[1:])
            a=np.max(list1[0],axis=0)
            if a[0]=='World':
                world=list1[0]
            if a[0]=='China':
                china=list1[0]
            dict2[i[0]]=a[3]
        wy=[]#世界
        wx=[]
        dy=[]
        ymy=[]#接种疫苗一针
        ym1=[]
        ym2=[]
        ym3=[]
        ym4=[]
        world=world.tolist()
        # print(type(world))
        for i in world:
            # if i[1] in self.month:
            wy.append(i[3])
            wx.append(i[1])
            ymy.append(i[5])
            ym1.append(i[6])
            ym2.append(i[7])
            ym3.append(i[8])
            ym4.append(i[9])
        ymyc = []  # 接种疫苗一针
        ym1c = []
        ym2c = []
        ym3c= []
        ym4c= []
        china = china.tolist()
        for i in china:
            # if i[1] in self.month:
            ymyc.append(i[5])
            ym1c.append(i[6])
            ym2c.append(i[7])
            ym3c.append(i[8])
            ym4c.append(i[9])
        # print(len(wy),len(wx))
        for i in self.l1:
            if i[1] =='2022-03-11':
                dict[i[0]]=i[2]
        cname=[]
        cnum=[]
        total_c=[]
        for i in dict.keys():
            cname.append(i)
            cnum.append(dict[i])
            total_c.append(dict2[i])
        for i in range(len(cnum)):
            if cname[i]=='South Korea':
                cname[i]='Korea'
            if cname[i]=='French Polynesia':
                cname[i]='Fr. Polynesia'
            if cname[i]=='Dominican Republic':
                cname[i]='Dominican Rep.'
            if cname[i]=='Falkland Islands':
                cname[i]='Falkland Is.'
            if cname[i]=='Solomon Islands':
                cname[i]='Solomon Is.'
            if cname[i]=='Timor':
                cname[i]='Timor-Leste'
            if cname[i] == 'Central African Republic':
                cname[i] = 'Central African Rep.'
            if cname[i]=='Laos':
                cname[i]='Lao PDR'
            if cname[i]=='Democratic Republic of Congo':
                cname[i]='Dem. Rep. Congo'
            if cname[i]=='South Sudan':
                cname[i]='S. Sudan'
            if cname[i]=='Cote d\'Ivoire':
                cname[i]='Côte d\'Ivoire'
            if cname[i]=='Bosnia and Herzegovina':
                cname[i]='Bosnia and Herz.'
            if cname[i] == 'Czechia':
                cname[i] = 'Czech Rep.'
        map_chart = Map()
        map_chart.add("截止2022-3-11全球各国新冠确诊人数",[list(z) for z in zip(cname,cnum)],'world',is_map_symbol_show=False)
        map_chart.set_series_opts(label_opts=opts.LabelOpts(is_show=False))
        map_chart.set_global_opts(title_opts=opts.TitleOpts(title="世界地图"),
                visualmap_opts=opts.VisualMapOpts(
                max_=10000000000,
                is_piecewise=True,
                pieces=[
                    {"min": 1, "max": 10000, "label": "10000人以下", "color": "#FFE6BE"},
                    {"min": 10000, "max": 100000, "label": "10000-100000人", "color": "#FFB769"},
                    {"min": 100000, "max": 1000000, "label": "100000-1000000人", "color": "#FF8F66"},
                    {"min": 1000000, "max": 10000000, "label": "100000-10000000人", "color": "#ED514E"},
                    {"min": 10000000, "max": 10000000000, "label": "10000000人以上", "color": "#CA0D11"}
                ]))
        attr1 = ["10000人以下", "10000-100000人", "100000-1000000人", "100000-10000000人", "10000000人以上"]
        pi1 = [0, 0, 0, 0, 0]
        for i in range(len(cnum)):
            if cname[i] in self.cun:
                if cnum[i] < 10000:
                    pi1[0] += 1
                if cnum[i] >= 10000 and cnum[i] < 100000:
                    pi1[1] += 1
                if cnum[i] >= 100000 and cnum[i] < 1000000:
                    pi1[2] += 1
                if cnum[i] >= 1000000 and cnum[i] < 10000000:
                    pi1[3] += 1
                if cnum[i] >= 10000000:
                    pi1[4] += 1
        c1 = (
            Pie()
                .add("", [list(z) for z in zip(attr1, pi1)])
                .set_global_opts(title_opts=opts.TitleOpts(title="感染人数"))
                .set_series_opts(label_opts=opts.LabelOpts(formatter="{b}: {d}%"))
        )
        map1 = Map()
        map1.add("截止2022-3-11全球接种疫苗数", [list(z) for z in zip(cname, total_c)], 'world', is_map_symbol_show=False)
        map1.set_series_opts(label_opts=opts.LabelOpts(is_show=False))
        map1.set_global_opts(title_opts=opts.TitleOpts(title="世界地图"),
                                  visualmap_opts=opts.VisualMapOpts(
                                      max_=10000000000,
                                      is_piecewise=True,
                                      pieces=[
                                          {"min": 1, "max": 100000, "label": "100000人以下", "color": "#FFE6BE"},
                                          {"min": 100000, "max": 1000000, "label": "100000-1000000人", "color": "#FFB769"},
                                          {"min": 1000000, "max": 10000000, "label": "1000000-10000000人", "color": "#FF8F66"},
                                          {"min": 10000000, "max": 100000000, "label": "1000000-100000000人",
                                           "color": "#ED514E"},
                                          {"min": 100000000, "max": 100000000000, "label": "100000000人以上",
                                           "color": "#CA0D11"}
                                      ]))
        x=[]
        y=[]
        attr=["100000人以下","100000-1000000人","1000000-10000000人","1000000-100000000人","100000000人以上"]
        pi=[0,0,0,0,0]
        for i in range(len(total_c)):
            if cname[i] in self.cun:
                if total_c[i]<10000:
                    pi[0]+=1
                if total_c[i]>=10000 and total_c[i]< 1000000 :
                    pi[1]+=1
                if total_c[i]>=1000000 and total_c[i]< 10000000 :
                    pi[2]+=1
                if total_c[i]>=10000000 and total_c[i]< 100000000 :
                    pi[3]+=1
                if total_c[i]>=100000000 :
                    pi[4]+=1
        for i in self.l2:
            if i[1]=='World':
                # if i[0] in self.month:
                x.append(i[0])
                y.append(i[2])
                dy.append(i[3])
        c = (
            Pie()
                .add("", [list(z) for z in zip(attr, pi)])
                .set_global_opts(title_opts=opts.TitleOpts(title="接种数"))
                .set_series_opts(label_opts=opts.LabelOpts(formatter="{b}:{d}%"))
        )
        line=(Line()
            .add_xaxis(xaxis_data=x)
            .add_yaxis(series_name="世界感染新冠人数折线图", y_axis=y, is_smooth=True,markpoint_opts=opts.MarkPointOpts(data=[opts.MarkPointItem(type_="max",name="最大值",symbol_size=105),##设置最大值 标记
                                                                ]
                                                          ,symbol='pin'
                                                            ))
            .set_global_opts(title_opts=opts.TitleOpts(title="世界感染新冠人数折线图"),yaxis_opts=opts.AxisOpts(name = '人数（人）'), xaxis_opts=opts.AxisOpts(
                        type_ = 'category',
                        name = '日期',
                        is_show = True,
                        is_scale = False,
                        is_inverse = False,
                        name_location = 'end',
                        name_gap = 35,
                        name_rotate = 30,  #旋转30度
                        interval= None,
                        grid_index = 0,
                        position = 'bottom',
                        offset = 0,
                        split_number = 5,
                        boundary_gap = None,
                        min_  = None,
                        max_ = None,
                        min_interval = 0,
                        max_interval = None),datazoom_opts=[
                opts.DataZoomOpts(
                    is_show=False, type_="inside",pos_bottom="-2%", xaxis_index=[0, 0], range_start=98, range_end=100)])
                 )
        bar=(Bar()
             .add_xaxis(xaxis_data=x)
             .add_yaxis(series_name='世界感染新冠人数柱形图',y_axis=y)
             # .add_yaxis(series_name='中国感染新冠人数柱形图', y_axis=cy)
             .set_global_opts(title_opts=opts.TitleOpts(title='世界感染新冠人数'),yaxis_opts=opts.AxisOpts(name = '人数（人）'), xaxis_opts=opts.AxisOpts(
                        type_ = 'category',
                        name = '日期',
                        is_show = True,
                        is_scale = False,
                        is_inverse = False,
                        name_location = 'end',
                        name_gap = 35,
                        name_rotate = 30,  #旋转30度
                        interval= None,
                        grid_index = 0,
                        position = 'bottom',
                        offset = 0,
                        split_number = 5,
                        boundary_gap = None,
                        min_  = None,
                        max_ = None,
                        min_interval = 0,
                        max_interval = None),datazoom_opts=[
                opts.DataZoomOpts(
                    is_show=False, type_="inside",pos_bottom="-2%", xaxis_index=[0, 0], range_start=98, range_end=100)])
             .set_series_opts(label_opts=opts.LabelOpts(is_show=False)))
        line1=(Line()
            .add_xaxis(xaxis_data=x)
            .add_yaxis(series_name="世界接种疫苗总数", y_axis=wy, is_smooth=True,markpoint_opts=opts.MarkPointOpts(data=[opts.MarkPointItem(type_="max",name="最大值",symbol_size=125),##设置最大值 标记
                                                                ]
                                                          ,symbol='pin'
                                                            ))
            .add_yaxis(series_name="接种过至少一剂疫苗的总人数", y_axis=ymy, is_smooth=True,markpoint_opts=opts.MarkPointOpts(data=[opts.MarkPointItem(type_="max",name="最大值",symbol_size=125),##设置最大值 标记
                                                                ]
                                                          ,symbol='pin'
                                                            ))
            .set_global_opts(title_opts=opts.TitleOpts(title="世界接种疫苗总数折线图"),yaxis_opts=opts.AxisOpts(name = '人数（人）'), xaxis_opts=opts.AxisOpts(
                        type_ = 'category',
                        name = '日期',
                        is_show = True,
                        is_scale = False,
                        is_inverse = False,
                        name_location = 'end',
                        name_gap = 35,
                        name_rotate = 30,  #旋转30度
                        interval= None,
                        grid_index = 0,
                        position = 'bottom',
                        offset = 0,
                        split_number = 5,
                        boundary_gap = None,
                        min_  = None,
                        max_ = None,
                        min_interval = 0,
                        max_interval = None),
            datazoom_opts=[
                opts.DataZoomOpts(
                    is_show=False, type_="inside",pos_bottom="-2%", xaxis_index=[0, 0], range_start=98, range_end=100)]))
        line2 = (Line()
                 .add_xaxis(xaxis_data=x)
                 .add_yaxis(series_name="世界因新冠死亡人数", y_axis=dy, is_smooth=True,markpoint_opts=opts.MarkPointOpts(data=[opts.MarkPointItem(type_="max",name="最大值",symbol_size=115),##设置最大值 标
                                                                ]
                                                          ,symbol='pin'
                                                            ))
                 .set_global_opts(title_opts=opts.TitleOpts(title="世界因新冠死亡人数折线图"),yaxis_opts=opts.AxisOpts(name = '人数（人）'), xaxis_opts=opts.AxisOpts(
                        type_ = 'category',
                        name = '日期',
                        is_show = True,
                        is_scale = False,
                        is_inverse = False,
                        name_location = 'end',
                        name_gap = 35,
                        name_rotate = 30,  #旋转30度
                        interval= None,
                        grid_index = 0,
                        position = 'bottom',
                        offset = 0,
                        split_number = 5,
                        boundary_gap = None,
                        min_  = None,
                        max_ = None,
                        min_interval = 0,
                        max_interval = None),datazoom_opts=[
                opts.DataZoomOpts(
                    is_show=False, type_="inside",pos_bottom="-2%", xaxis_index=[0, 0], range_start=98, range_end=100)])
                 )
        line3 = (Line()
                 .add_xaxis(xaxis_data=x)
                 .add_yaxis(series_name="接受初始疫苗接种方案规定的所有剂量的总人数", y_axis=ym1, is_smooth=True)
                 .add_yaxis(series_name="COVID-19 疫苗加强剂总数", y_axis=ym2, is_smooth=True)
                 .add_yaxis(series_name="总人口中每 100 人接种的 COVID-19 疫苗总数", y_axis=ym3, is_smooth=True)
                 .add_yaxis(series_name="总人口中每 100 人接种的 COVID-19 疫苗加强剂总数", y_axis=ym4, is_smooth=True)
                 .set_global_opts(title_opts=opts.TitleOpts(title="世界接种疫苗总数折线图"),yaxis_opts=opts.AxisOpts(name = '人数（人）'), xaxis_opts=opts.AxisOpts(
                        type_ = 'category',
                        name = '日期',
                        is_show = True,
                        is_scale = False,
                        is_inverse = False,
                        name_location = 'end',
                        name_gap = 35,
                        name_rotate = 30,  #旋转30度
                        interval= None,
                        grid_index = 0,
                        position = 'bottom',
                        offset = 0,
                        split_number = 5,
                        boundary_gap = None,
                        min_  = None,
                        max_ = None,
                        min_interval = 0,
                        max_interval = None),
                                  datazoom_opts=[
                                      opts.DataZoomOpts(
                                          is_show=False, type_="inside", pos_bottom="-2%", xaxis_index=[0, 0],
                                          range_start=98, range_end=100)]))
        line4 = (Line()
                 .add_xaxis(xaxis_data=x)
                 .add_yaxis(series_name="中国接受初始疫苗接种方案规定的所有剂量的总人数", y_axis=ym1c, is_smooth=True)
                 .add_yaxis(series_name="中国COVID-19 疫苗加强剂总数", y_axis=ym2c, is_smooth=True)
                 .add_yaxis(series_name="中国总人口中每 100 人接种的 COVID-19 疫苗总数", y_axis=ym3c, is_smooth=True)
                 .add_yaxis(series_name="中国总人口中每 100 人接种的 COVID-19 疫苗加强剂总数", y_axis=ym4c, is_smooth=True)
                 .set_global_opts(title_opts=opts.TitleOpts(title="中国接种疫苗总数折线图"),yaxis_opts=opts.AxisOpts(name = '人数（人）'), xaxis_opts=opts.AxisOpts(
                        type_ = 'category',
                        name = '日期',
                        is_show = True,
                        is_scale = False,
                        is_inverse = False,
                        name_location = 'end',
                        name_gap = 35,
                        name_rotate = 30,  #旋转30度
                        interval= None,
                        grid_index = 0,
                        position = 'bottom',
                        offset = 0,
                        split_number = 5,
                        boundary_gap = None,
                        min_  = None,
                        max_ = None,
                        min_interval = 0,
                        max_interval = None),
                                  datazoom_opts=[
                                      opts.DataZoomOpts(
                                          is_show=False, type_="inside", pos_bottom="-2%", xaxis_index=[0, 0],
                                          range_start=98, range_end=100)]))

        all=bar.overlap(line)
        page = Page(layout=Page.DraggablePageLayout)
        page.add(map_chart,c1,map1,c,all,line1,line2,line3,line4)
        page.render('世界地图.html')
        os.system("世界地图.html")
covid()
class china():
    def __init__(self):
        self.ch=[]
        self.cont=[]
        self.pdc=[]
        self.l1=[]#全国中国消费物价指数
        self.l2=[]#城市
        self.l3=[]#农村
        self.l4=[]#GDP
        self.l5=[]#gdp增长指数
        self.page = Page(layout=Page.DraggablePageLayout)
        self.month = ['2020-01-31', '2020-02-29', '2020-03-31', '2020-04-30', '2020-05-31', '2020-06-30', '2020-07-31',
                      '2020-08-31', '2020-09-30',
                      '2020-10-31', '2020-11-30', '2020-12-31',
                      '2021-01-31', '2021-02-28', '2021-03-31', '2021-04-30', '2021-05-31', '2021-06-30', '2021-07-31',
                      '2021-08-31',
                      '2021-09-30', '2021-10-31', '2021-11-30', '2021-12-31', '2022-01-31', '2022-02-28', '2022-03-11'
                      ]
        self.yuanshiyiq()
        self.jingj()
    def yuanshiyiq(self):
        path = 'E:\学习\课程设计三\owid-covid-data.csv'
        df = pd.read_csv(path, index_col=0)
        l = df.loc[:, ['location', 'date', 'total_cases', 'total_vaccinations', 'total_deaths','people_vaccinated','total_boosters','total_vaccinations_per_hundred','people_vaccinated_per_hundred']]
        group = l.groupby("location")
        self.cont = list(group)
        for i in self.cont:
            array=np.array(i[1:])
            list1=array.tolist()
            if list1[0][0][0]=='China':
                self.ch=array
                break
        x0=[]
        x=[]
        y1=[]
        y2=[]
        y3=[]
        self.ch.tolist()
        print(self.ch)
        for i in self.ch[0]:
            x.append(i[1])
            if i[1] in self.month:
                x0.append(i[1])
                y1.append(i[2])
                y3.append(i[4])
            y2.append(i[3])
        # print(self.ch.tolist())
        line = (Line()
                .add_xaxis(xaxis_data=x0)
                .add_yaxis(series_name="中国感染新冠人数", y_axis=y1, is_smooth=True)
                .add_yaxis(series_name="中国因新冠死亡人数", y_axis=y3, is_smooth=True)
                .set_global_opts(title_opts=opts.TitleOpts(title="中国感染新冠人数折线图"),yaxis_opts=opts.AxisOpts(name = '人数（人）'), xaxis_opts=opts.AxisOpts(
                        type_ = 'category',
                        name = '日期',
                        is_show = True,
                        is_scale = False,
                        is_inverse = False,
                        name_location = 'end',
                        name_gap = 35,
                        name_rotate = 30,  #旋转30度
                        interval= None,
                        grid_index = 0,
                        position = 'bottom',
                        offset = 0,
                        split_number = 5,
                        boundary_gap = None,
                        min_  = None,
                        max_ = None,
                        min_interval = 0,
                        max_interval = None),datazoom_opts=[
                opts.DataZoomOpts(
                    is_show=False, type_="inside",pos_bottom="-2%", xaxis_index=[0, 0], range_start=98, range_end=100)]))
        line1 = (Line()
                 .add_xaxis(xaxis_data=x)
                 .add_yaxis(series_name="中国接种疫苗总数", y_axis=y2, is_smooth=True)
                 .set_global_opts(title_opts=opts.TitleOpts(title="中国接种疫苗总数折线图"),yaxis_opts=opts.AxisOpts(name = '人数（人）'), xaxis_opts=opts.AxisOpts(
                        type_ = 'category',
                        name = '日期',
                        is_show = True,
                        is_scale = False,
                        is_inverse = False,
                        name_location = 'end',
                        name_gap = 35,
                        name_rotate = 30,  #旋转30度
                        interval= None,
                        grid_index = 0,
                        position = 'bottom',
                        offset = 0,
                        split_number = 5,
                        boundary_gap = None,
                        min_  = None,
                        max_ = None,
                        min_interval = 0,
                        max_interval = None),datazoom_opts=[
                opts.DataZoomOpts(
                    is_show=False, type_="inside",pos_bottom="-2%", xaxis_index=[0, 0], range_start=98, range_end=100)])
                 )
        bar = (Bar()
               .add_xaxis(xaxis_data=x0)
               .add_yaxis(series_name='中国感染新冠人数柱形图', y_axis=y1)
               .add_yaxis(series_name='中国因新冠死亡人数柱形图', y_axis=y3)
               .set_global_opts(title_opts=opts.TitleOpts(title='世界感染新冠人数柱形图'),yaxis_opts=opts.AxisOpts(name = '人数（人）'), xaxis_opts=opts.AxisOpts(
                        type_ = 'category',
                        name = '日期',
                        is_show = True,
                        is_scale = False,
                        is_inverse = False,
                        name_location = 'end',
                        name_gap = 35,
                        name_rotate = 30,  #旋转30度
                        interval= None,
                        grid_index = 0,
                        position = 'bottom',
                        offset = 0,
                        split_number = 5,
                        boundary_gap = None,
                        min_  = None,
                        max_ = None,
                        min_interval = 0,
                        max_interval = None),datazoom_opts=[
                opts.DataZoomOpts(
                    is_show=False, type_="inside",pos_bottom="-2%", xaxis_index=[0, 0], range_start=98, range_end=100)])
               .set_series_opts(label_opts=opts.LabelOpts(is_show=False)))
        # line2 = (Line()
        #          .add_xaxis(xaxis_data=x)
        #          .add_yaxis(series_name="中国因新冠死亡人数", y_axis=y3, is_smooth=True)
        #          .set_global_opts(title_opts=opts.TitleOpts(title="中国因新冠死亡人数折线图"))
        #          )
        all=line.overlap(bar)
        self.page.add(all, line1)
        # page.render('中国地图.html')
        # os.system("中国地图.html")
    def jingj(self):
        path='E:\学习\课程设计三\gmjj\CPI.csv'
        df = pd.read_csv(path)
        allc=df.loc[:,['Month','Nation_Current_Month','Nation_YOY','Nation_Comparative_Rate','Nation_Total']]
        allch=df.loc[:,['Month','City_Current_Month','City_YOY','City_Comparative_Rate','City_Total']]
        allnc = df.loc[:, ['Month', 'Country_Current_Month', 'Country_YOY', 'Country_Comparative_Rate', 'Country_Total']]
        dataa = np.array(allnc)
        self.l3 = dataa.tolist()
        dataa = np.array(allc)
        self.l1 = dataa.tolist()
        dataa = np.array(allch)
        self.l2 = dataa.tolist()
        print(self.l1)
        self.gdp()
        self.prch()
    def gdp(self):
        path = 'E:\学习\课程设计三\gmjj\GDP.csv'
        df = pd.read_csv(path)
        print(df)
        allc=df.loc[:,['Quater','GDP_Absolute','Primary_Indusry_Abs','Secondary_Indusry_Abs','Tertiary_Indusry_Abs']]
        allch=df.loc[:,['Quater','GDP_YOY','Primary_Indusry_YOY','Secondary_Indusry_YOY','Tertiary_Indusry_YOY']]
        dataa = np.array(allc)
        self.l4 = dataa.tolist()
        dataa = np.array(allch)
        self.l5 = dataa.tolist()
        self.gdpp()
    def gdpp(self):
        x = []
        y1 = []
        y2 = []
        y3 = []
        y4 = []
        yy1 = []
        yy2 = []
        yy3 = []
        yy4 = []
        self.l4.reverse()
        self.l5.reverse()
        for i in range(0,len(self.l4)):
            x.append(self.l4[i][0])
            y1.append(self.l4[i][1])
            y2.append(str(self.l4[i][2]))
            y3.append(str(self.l4[i][3]))
            y4.append(self.l4[i][4])
            yy1.append(str(self.l5[i][1]).replace('%',''))
            yy2.append(str(self.l5[i][2]).replace('%',''))
            yy3.append(str(self.l5[i][3]).replace('%',''))
            yy4.append(str(self.l5[i][4]).replace('%',''))
        line = (Line()
                .add_xaxis(xaxis_data=x)
                .add_yaxis(series_name="国内生产总值绝对值", y_axis=y1, is_smooth=True)
                .add_yaxis(series_name="第一产业绝对值_亿元", y_axis=y2, is_smooth=True)
                .add_yaxis(series_name="第二产业绝对值_亿元", y_axis=y3, is_smooth=True)
                .add_yaxis(series_name="第三产业绝对值_亿元", y_axis=y4, is_smooth=True)
                .set_series_opts(label_opts=opts.LabelOpts(is_show=False))
                .set_global_opts(title_opts=opts.TitleOpts(title="GDP总值"),yaxis_opts=opts.AxisOpts(name = '价值（亿元）'), xaxis_opts=opts.AxisOpts(
                        type_ = 'category',
                        name = '日期',
                        is_show = True,
                        is_scale = False,
                        is_inverse = False,
                        name_location = 'end',
                        name_gap = 35,
                        name_rotate = 30,  #旋转30度
                        interval= None,
                        grid_index = 0,
                        position = 'bottom',
                        offset = 0,
                        split_number = 5,
                        boundary_gap = None,
                        min_  = None,
                        max_ = None,
                        min_interval = 0,
                        max_interval = None),datazoom_opts=[
                opts.DataZoomOpts(
                    is_show=False, type_="inside",pos_bottom="-2%", xaxis_index=[0, 0], range_start=98, range_end=100)]))
        line1 = (Line()
                 .add_xaxis(xaxis_data=x)
                 .add_yaxis(series_name="国内生产总值同比增长", y_axis=yy1, is_smooth=True)
                 .add_yaxis(series_name="第一产业同比增长", y_axis=yy2, is_smooth=True)
                 .add_yaxis(series_name="第二产业同比增长", y_axis=yy3, is_smooth=True)
                 .add_yaxis(series_name="第三产业同比增长", y_axis=yy4, is_smooth=True)
                 .set_series_opts(label_opts=opts.LabelOpts(is_show=False))
                 .set_global_opts(title_opts=opts.TitleOpts(title="GDP同比增长"),yaxis_opts=opts.AxisOpts(name = '增长率（%）'), xaxis_opts=opts.AxisOpts(
                        type_ = 'category',
                        name = '日期',
                        is_show = True,
                        is_scale = False,
                        is_inverse = False,
                        name_location = 'end',
                        name_gap = 35,
                        name_rotate = 30,  #旋转30度
                        interval= None,
                        grid_index = 0,
                        position = 'bottom',
                        offset = 0,
                        split_number = 5,
                        boundary_gap = None,
                        min_  = None,
                        max_ = None,
                        min_interval = 0,
                        max_interval = None),datazoom_opts=[
                            opts.DataZoomOpts(
                                is_show=False, type_="inside",pos_bottom="-2%", xaxis_index=[0, 0], range_start=98, range_end=100)]))
        self.page.add(line, line1)
    def prch(self):#全国消费物价指数
        x=[]
        y1=[]
        y2=[]
        y3=[]
        y4=[]
        yy1 = []
        yy2 = []
        yy3 = []
        yy4 = []
        self.l3.reverse()
        yyy1 = []
        yyy2 = []
        yyy3 = []
        yyy4 = []
        self.l1.reverse()
        self.l2.reverse()
        for i in range(0,len(self.l1)):
            x.append(self.l1[i][0])
            y1.append(self.l1[i][1])
            y2.append(str(self.l1[i][2]).replace('%',''))
            y3.append(str(self.l1[i][3]).replace('%',''))
            y4.append(self.l1[i][4])
            yy1.append(self.l2[i][1])
            yy2.append(str(self.l2[i][2]).replace('%', ''))
            yy3.append(str(self.l2[i][3]).replace('%', ''))
            yy4.append(self.l2[i][4])
            yyy1.append(self.l3[i][1])
            yyy2.append(str(self.l3[i][2]).replace('%', ''))
            yyy3.append(str(self.l3[i][3]).replace('%', ''))
            yyy4.append(self.l3[i][4])
        print(y2)
        line = (Line()
                .add_xaxis(xaxis_data=x)
                .add_yaxis(series_name="全国当月", y_axis=y1, is_smooth=True)
                .add_yaxis(series_name="全国累计", y_axis=y4, is_smooth=True)
                .add_yaxis(series_name="城市当月", y_axis=yy1, is_smooth=True)
                .add_yaxis(series_name="城市累计", y_axis=yy4, is_smooth=True)
                .add_yaxis(series_name="农村当月", y_axis=yyy1, is_smooth=True)
                .add_yaxis(series_name="农村累计", y_axis=yyy4, is_smooth=True)
                .set_series_opts(label_opts=opts.LabelOpts(is_show=False))
                .set_global_opts(title_opts=opts.TitleOpts(title="全国消费物价指数"),yaxis_opts=opts.AxisOpts(name = '价格（亿元）'), xaxis_opts=opts.AxisOpts(
                        type_ = 'category',
                        name = '日期',
                        is_show = True,
                        is_scale = False,
                        is_inverse = False,
                        name_location = 'end',
                        name_gap = 35,
                        name_rotate = 30,  #旋转30度
                        interval= None,
                        grid_index = 0,
                        position = 'bottom',
                        offset = 0,
                        split_number = 5,
                        boundary_gap = None,
                        min_  = None,
                        max_ = None,
                        min_interval = 0,
                        max_interval = None),datazoom_opts=[
                opts.DataZoomOpts(
                    is_show=False, type_="inside",pos_bottom="-2%", xaxis_index=[0, 0], range_start=98, range_end=100)]))
        line1 = (Line()
                .add_xaxis(xaxis_data=x)
                .add_yaxis(series_name="全国同比增长", y_axis=y2, is_smooth=True)
                .add_yaxis(series_name="全国环比增长", y_axis=y3, is_smooth=True)
                 .add_yaxis(series_name="城市同比增长", y_axis=yy2, is_smooth=True)
                 .add_yaxis(series_name="城市环比增长", y_axis=yy3, is_smooth=True)
                 .add_yaxis(series_name="农村同比增长", y_axis=yyy2, is_smooth=True)
                 .add_yaxis(series_name="农村环比增长", y_axis=yyy3, is_smooth=True)
                .set_series_opts(label_opts=opts.LabelOpts(is_show=False))
                .set_global_opts(title_opts=opts.TitleOpts(title="全国消费物价指数(%)"),yaxis_opts=opts.AxisOpts(name = '增长率（%）'), xaxis_opts=opts.AxisOpts(
                        type_ = 'category',
                        name = '日期',
                        is_show = True,
                        is_scale = False,
                        is_inverse = False,
                        name_location = 'end',
                        name_gap = 35,
                        name_rotate = 30,  #旋转30度
                        interval= None,
                        grid_index = 0,
                        position = 'bottom',
                        offset = 0,
                        split_number = 5,
                        boundary_gap = None,
                        min_  = None,
                        max_ = None,
                        min_interval = 0,
                        max_interval = None),datazoom_opts=[
                opts.DataZoomOpts(
                    is_show=False, type_="inside",pos_bottom="-2%", xaxis_index=[0, 0], range_start=98, range_end=100)]))
        self.page.add(line,line1)
        self.page.render('中国消费物价指数.html')
        os.system("中国消费物价指数.html")
china()
class  ciyut():
    def __init__(self,list1):
        self.path=list1
        self.dic={}
        self.key=[]
        self.openfile()
    def openfile(self):
        for i in self.path:
            for j in i:
                try:
                    f=open(j,'r',encoding='utf-8')
                    str=f.read()
                    l=jieba.cut(str)
                    keywords20=[]
                    for i in l:
                        if i not in stopw:
                            keywords20.append(i)
                    str1=''.join(keywords20)
                    keywords20 = jieba.analyse.extract_tags(str1,topK=5)
                    l = list(filter(lambda x: not x.isdigit(), keywords20))
                    self.key.extend(l)
                except:
                    pass
        for i in self.key:
            self.dic[i]=self.dic.get(i,0)+1
        with open('ciyun.json','w') as f1:
            json_s=json.dumps(self.dic,ensure_ascii = False)
            f1.write(json_s)
def ciyuntu():
    list1 = []
    path = 'E:\学习\课程设计三\china_policy'
    for root, dir, files in os.walk(path):
        l = []
        for file in files:
            l.append(os.path.join(root, file))
        if len(l) != 0:
            list1.append(l)
    ciyut(list1)
def print_c():
    f=open('ciyun.json','r')
    dic=json.load(f)
    my_cloud = WordCloud(
        background_color='white',  # 设置背景颜色  默认是black
        width=900, height=600,
        max_words=100,  # 词云显示的最大词语数量
        font_path='simhei.ttf',  # 设置字体  显示中文
        max_font_size=99,  # 设置字体最大值
        min_font_size=16,  # 设置子图最小值
        random_state=50  # 设置随机生成状态，即多少种配色方案
    ).generate_from_frequencies(dic)
    plt.imshow(my_cloud, interpolation='bilinear')
    # 显示设置词云图中无坐标轴
    plt.axis('off')
    plt.show()
    my_cloud.to_file('中国防疫政策词云图.jpg')
# ciyuntu()
# print_c()
