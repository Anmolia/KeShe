import json
from pyecharts.charts import Line, Page, Bar
from wordcloud import WordCloud
import os
import jieba.analyse
import matplotlib.pyplot as plt
import sklearn
import numpy as np
import pandas as pd
from pyecharts.charts import Map
from pyecharts import options as opts
stopw=['以上','浏览器','9.0','做好','之']
class covid():
    def __init__(self):
        self.l1=[]
        self.l2=[]
        self.cont=[]
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
        l=df.loc[:,['location','date','total_cases','total_vaccinations']]
        l2=df.loc[:,['date','location','total_cases']]
        l = l.fillna(0)
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
        for i in self.cont:
            list1=np.array(i[1:])
            a=np.max(list1[0],axis=0)
            if a[0]=='World':
                world=list1[0]
            dict2[i[0]]=a[3]
        wy=world[:,3]
        wx=world[:,1]
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
        map_chart.add("截止2022-3-11全球接种疫苗数", [list(z) for z in zip(cname, total_c)], 'world', is_map_symbol_show=False)
        map_chart.set_series_opts(label_opts=opts.LabelOpts(is_show=False))
        map_chart.set_global_opts(title_opts=opts.TitleOpts(title="世界地图"),
                visualmap_opts=opts.VisualMapOpts(
                max_=10000000000,
                is_piecewise=True,
                pieces=[
                    {"min": 1, "max": 10000, "label": "1000人以下", "color": "#FFE6BE"},
                    {"min": 10000, "max": 100000, "label": "1000-10000人", "color": "#FFB769"},
                    {"min": 100000, "max": 1000000, "label": "10000-100000人", "color": "#FF8F66"},
                    {"min": 1000000, "max": 10000000, "label": "10000-1000000人", "color": "#ED514E"},
                    {"min": 10000000, "max": 10000000000, "label": "1000000人以上", "color": "#CA0D11"}
                ]))
        x=[]
        y=[]
        for i in self.l2:
            if i[1]=='World':
                if i[0] in self.month:
                    x.append(i[0])
                    y.append(i[2])
        line=(Line()
            .add_xaxis(xaxis_data=x)
            .add_yaxis(series_name="y线", y_axis=y, is_smooth=True)
            .set_global_opts(title_opts=opts.TitleOpts(title="Line-折线重叠")))
        bar=(Bar()
             .add_xaxis(xaxis_data=x)
             .add_yaxis(series_name='y',y_axis=y)
             .set_global_opts(title_opts=opts.TitleOpts(title='柱形图'))
             .set_series_opts(label_opts=opts.LabelOpts(is_show=False)))
        line1=(Line()
            .add_xaxis(xaxis_data=wx)
            .add_yaxis(series_name="y线", y_axis=wy, is_smooth=True)
            .set_global_opts(title_opts=opts.TitleOpts(title="Line-折线重叠"))
               )
        all=bar.overlap(line)
        page = Page(layout=Page.DraggablePageLayout)
        page.add(map_chart,all)
        page.render('世界地图.html')
        os.system("世界地图.html")
covid()
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
                    keywords20 = jieba.analyse.extract_tags(str1,topK=10)
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
print_c()
