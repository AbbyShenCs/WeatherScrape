import pandas as pd
from pyecharts.charts import Map
import pyecharts.options as opts

frame = pd.read_csv("done.csv")
map = Map()
map.add("temperature",frame[["province","temperature"]].values.tolist(),"china")
map.set_global_opts(visualmap_opts=opts.VisualMapOpts(min_=-25,max_=25))
map.render("2021年12月23日全国各地区省日平均气温图.html")
