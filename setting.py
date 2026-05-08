from pyecharts.charts import Page
page=Page(layout=Page.DraggablePageLayout,page_title='全国出游信息')
page.save_resize_html("index.html",cfg_file="chart_config.json",dest="全国出游信息大屏可视化.html")