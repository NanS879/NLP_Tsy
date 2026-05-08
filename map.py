# ==========================================
# 中国旅游景点数据可视化分析
# ==========================================

# ========= 导入库 =========

import pandas as pd
import jieba

from collections import Counter

from pyecharts import options as opts

from pyecharts.charts import (
    Bar,
    Pie,
    Map,
    WordCloud,
    Page
)


# ==========================================
# 1. 读取数据
# ==========================================

df = pd.read_excel("data(5)/data/旅游景点.xlsx")


# ==========================================
# 2. 数据清洗
# ==========================================

# 查看空缺值
print("===== 空缺值统计 =====")
print(df.isnull().sum())

# 填充星级空值
df["星级"] = df["星级"].fillna("未知")

# 删除销量为0的数据
df = df[df["销量"] != 0]

# 保存新数据
df.to_excel("newData.xlsx", index=False)

print("\n数据清洗完成！")


# ==========================================
# 3. 高级景点分布（柱状图）
# ==========================================

# 筛选4A和5A景点
high_level = df[df["星级"].isin(["4A", "5A"])]

# 按城市统计
city_count = high_level.groupby("城市").size()

bar1 = (
    Bar()

    .add_xaxis(city_count.index.tolist())

    .add_yaxis(
        "4A以上景点数量",
        city_count.values.tolist()
    )

    .set_global_opts(
        title_opts=opts.TitleOpts(
            title="高级景点分布"
        ),

        xaxis_opts=opts.AxisOpts(
            axislabel_opts=opts.LabelOpts(rotate=45)
        )
    )
)


# ==========================================
# 4. 热门旅游目的地（Top20）
# ==========================================

top20 = df.sort_values(
    by="销量",
    ascending=False
).head(20)

bar2 = (
    Bar()

    .add_xaxis(
        top20["名称"].tolist()
    )

    .add_yaxis(
        "销量",
        top20["销量"].tolist()
    )

    .reversal_axis()

    .set_global_opts(
        title_opts=opts.TitleOpts(
            title="销量Top20景点"
        )
    )
)


# ==========================================
# 5. 热门景点地图
# ==========================================

city_sale = df.groupby("城市")["销量"].sum()

data_pair = [
    list(z)
    for z in zip(
        city_sale.index.tolist(),
        city_sale.values.tolist()
    )
]

map_chart = (
    Map()

    .add(
        "景点销量",
        data_pair,
        "china-cities",

        label_opts=opts.LabelOpts(
            is_show=False
        )
    )

    .set_global_opts(

        title_opts=opts.TitleOpts(
            title="全国景点销量地图"
        ),

        visualmap_opts=opts.VisualMapOpts(
            max_=max(city_sale.values)
        )
    )
)


# ==========================================
# 6. 价格区间分析
# ==========================================

def price_level(price):

    if price <= 50:
        return "0-50元"

    elif price <= 100:
        return "50-100元"

    elif price <= 200:
        return "100-200元"

    else:
        return "200元以上"


# 添加价格区间列
df["价格区间"] = df["价格"].apply(price_level)


# ==========================================
# 7. 价格区间分布（饼图）
# ==========================================

price_count = df["价格区间"].value_counts()

price_data = list(zip(
    price_count.index.tolist(),
    price_count.values.tolist()
))

pie = (
    Pie()

    .add(
        "",
        price_data
    )

    .set_global_opts(
        title_opts=opts.TitleOpts(
            title="景点价格区间分布"
        )
    )

    .set_series_opts(
        label_opts=opts.LabelOpts(
            formatter="{b}: {c}"
        )
    )
)


# ==========================================
# 8. 价格与销量关系
# ==========================================

sale_price = df.groupby("价格区间")["销量"].sum()

bar3 = (
    Bar()

    .add_xaxis(
        sale_price.index.tolist()
    )

    .add_yaxis(
        "销量",
        sale_price.values.tolist()
    )

    .set_global_opts(
        title_opts=opts.TitleOpts(
            title="价格区间销量分析"
        )
    )
)


# ==========================================
# 9. 评分分布
# ==========================================

score_count = df["评分"].value_counts().sort_index()

bar4 = (
    Bar()

    .add_xaxis(
        [str(i) for i in score_count.index.tolist()]
    )

    .add_yaxis(
        "景点数量",
        score_count.values.tolist()
    )

    .set_global_opts(
        title_opts=opts.TitleOpts(
            title="景点评分分布"
        )
    )
)


# ==========================================
# 10. 词云图
# ==========================================

# 筛选评分4分以上景点
df_4 = df[df["评分"] > 4]

# 拼接简介
scene_intro = df_4["简介"].tolist()

scene_intro = " ".join(scene_intro)

# 分词
words = jieba.lcut(scene_intro)

# 读取停用词
with open(
    "data(5)/data/cn_stopwords.txt",
    encoding="utf-8"
) as f:

    stopwords = f.read().splitlines()

# 去除停用词
words = [
    word
    for word in words
    if word not in stopwords and len(word) > 1
]

# 统计词频
word_count = Counter(words)

word_list = list(word_count.items())

# 词云图
wordcloud = (
    WordCloud()

    .add(
        "",
        word_list,
        word_size_range=[20, 100]
    )

    .set_global_opts(
        title_opts=opts.TitleOpts(
            title="高评分景点词云图"
        )
    )
)


# ==========================================
# 11. Page整合
# ==========================================

page = Page(
    layout=Page.DraggablePageLayout
)

page.add(
    bar1,
    bar2,
    map_chart,
    pie,
    bar3,
    bar4,
    wordcloud
)


# ==========================================
# 12. 生成HTML
# ==========================================

page.render("index.html")