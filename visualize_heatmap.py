import pandas as pd
import folium
from folium.plugins import HeatMap

# 读取数据
df = pd.read_csv('surrounding_pois.csv')

# 提取经纬度
heat_data = []
for pos in df['POI位置']:
    try:
        lon, lat = map(float, str(pos).split(','))
        heat_data.append([lat, lon])
    except:
        continue

# 创建地图
m = folium.Map(location=[28.2, 112.98], zoom_start=12,
               tiles='https://webrd01.is.autonavi.com/appmaptile?lang=zh_cn&size=1&scale=1&style=7&x={x}&y={y}&z={z}',
               attr='高德地图')

# 添加热力图
HeatMap(heat_data, radius=16, blur=18, min_opacity=0.3, max_zoom=1).add_to(m)

# 保存
m.save('poi_heatmap.html')
print('已保存为 poi_heatmap.html，请在浏览器中打开查看') 