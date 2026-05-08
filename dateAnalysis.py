import pandas as pd
import matplotlib.pyplot as plt
import pyecharts.options as opts
from pyecharts.charts import Bar, Line, Grid
df = pd.read_excel(r'自然语言处理\data\旅游景点.xlsx',index_col=0)
df['星级']=df['星级'].fillna('未知')
df=df.loc[df['销量']>0]
df_4A=df.loc[df['星级'].isin(['4A','5A,'])]
df_4A_count=df_4A.groupby(by="城市")["名称"].count()
cities_name=df_4A_count.index.tolist()
cities_count=df_4A_count.values.tolist()
c=(
    Bar()
    .add_xaxis(cities_name)
    .add_yaxis("4A级及以上景点数量", cities_count)
    .set_global_opts(title_opts=opts.TitleOpts(title="4A、5A景点数量"))
)
c.render("景点统计结果.html")