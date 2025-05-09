import pandas as pd
import folium
from folium import plugins
import json

# 读取公园数据
parks_df = pd.read_csv('parks.csv')
# 读取周边POI数据
pois_df = pd.read_csv('surrounding_pois_20.csv')

# 打印数据信息
print("公园数据信息:")
print(parks_df[['name', 'location']].head())
print("\nPOI数据信息:")
print(pois_df[['POI名称', 'POI位置']].head())

# 创建地图，以长沙市中心为初始中心点
m = folium.Map(location=[28.2282, 112.9388], zoom_start=12, 
               tiles='https://webrd01.is.autonavi.com/appmaptile?lang=zh_cn&size=1&scale=1&style=7&x={x}&y={y}&z={z}',
               attr='高德地图')

# 添加公园标记
for idx, row in parks_df.iterrows():
    try:
        # 解析经纬度
        lon, lat = map(float, row['location'].split(','))
        
        # 创建弹出信息
        popup_html = f"""
        <div style='width: 200px; font-family: Arial, sans-serif;'>
            <h4 style='color: #2ecc71; margin-bottom: 10px;'>{row['name']}</h4>
            <p style='margin: 5px 0;'><b>地址:</b> {row['address']}</p>
            <p style='margin: 5px 0;'><b>评分:</b> {row['biz_ext'].split("'rating': '")[1].split("'")[0] if pd.notna(row['biz_ext']) else '暂无'}</p>
            <p style='margin: 5px 0;'><b>电话:</b> {row['tel'] if pd.notna(row['tel']) else '暂无'}</p>
        </div>
        """
        
        # 添加公园标记（绿色）
        folium.Marker(
            location=[lat, lon],
            popup=folium.Popup(popup_html, max_width=300),
            icon=folium.Icon(color='green', icon='tree-conifer', prefix='fa'),
            tooltip=row['name']
        ).add_to(m)
    except Exception as e:
        print(f"处理公园 {row['name']} 时出错: {e}")

# 添加POI标记
poi_colors = {
    '餐饮': 'red',
    '住宿': 'blue',
    '购物': 'purple',
    '学校': 'orange',
    '文体中心': 'pink',
    '公交地铁': 'gray'
}

poi_icons = {
    '餐饮': 'cutlery',
    '住宿': 'bed',
    '购物': 'shopping-cart',
    '学校': 'graduation-cap',
    '文体中心': 'star',
    '公交地铁': 'subway'
}

for idx, row in pois_df.iterrows():
    try:
        # 解析经纬度
        lon, lat = map(float, row['POI位置'].split(','))
        
        # 创建弹出信息
        popup_html = f"""
        <div style='width: 200px; font-family: Arial, sans-serif;'>
            <h4 style='color: #3498db; margin-bottom: 10px;'>{row['POI名称']}</h4>
            <p style='margin: 5px 0;'><b>类别:</b> {row['POI类别']}</p>
            <p style='margin: 5px 0;'><b>地址:</b> {row['POI地址']}</p>
            <p style='margin: 5px 0;'><b>评分:</b> {row['POI评分'] if pd.notna(row['POI评分']) else '暂无'}</p>
            <p style='margin: 5px 0;'><b>电话:</b> {row['POI电话'] if pd.notna(row['POI电话']) else '暂无'}</p>
            <p style='margin: 5px 0;'><b>距离公园:</b> {row['POI距离']}米</p>
        </div>
        """
        
        # 添加POI标记
        folium.Marker(
            location=[lat, lon],
            popup=folium.Popup(popup_html, max_width=300),
            icon=folium.Icon(color=poi_colors.get(row['POI类别'], 'gray'), 
                           icon=poi_icons.get(row['POI类别'], 'info-sign'),
                           prefix='fa'),
            tooltip=f"{row['POI类别']}: {row['POI名称']}"
        ).add_to(m)
    except Exception as e:
        print(f"处理POI {row['POI名称']} 时出错: {e}")

# 添加图例
legend_html = '''
<div style="position: fixed; 
            bottom: 20px; right: 20px; width: 130px; height: auto; 
            background-color: white; border:2px solid grey; z-index:9999;
            padding: 10px; font-family: Arial, sans-serif; font-size: 12px;
            border-radius: 5px; box-shadow: 0 0 10px rgba(0,0,0,0.2);">
    <p style='margin: 5px 0;'><i class="fa fa-tree-conifer" style="color:green"></i> 公园</p>
    <p style='margin: 5px 0;'><i class="fa fa-cutlery" style="color:red"></i> 餐饮</p>
    <p style='margin: 5px 0;'><i class="fa fa-bed" style="color:blue"></i> 住宿</p>
    <p style='margin: 5px 0;'><i class="fa fa-shopping-cart" style="color:purple"></i> 购物</p>
    <p style='margin: 5px 0;'><i class="fa fa-graduation-cap" style="color:orange"></i> 学校</p>
    <p style='margin: 5px 0;'><i class="fa fa-star" style="color:pink"></i> 文体中心</p>
    <p style='margin: 5px 0;'><i class="fa fa-subway" style="color:gray"></i> 公交地铁</p>
</div>
'''
m.get_root().html.add_child(folium.Element(legend_html))

# 添加标题
title_html = '''
<div style="position: fixed; 
            top: 20px; left: 50%; transform: translateX(-50%);
            background-color: white; border:2px solid grey; z-index:9999;
            padding: 10px; font-family: Arial, sans-serif; font-size: 16px;
            border-radius: 5px; box-shadow: 0 0 10px rgba(0,0,0,0.2);">
    <b>长沙市公园及周边设施分布图</b>
</div>
'''
m.get_root().html.add_child(folium.Element(title_html))

# 保存地图
m.save('parks_map.html')
print("\n地图已保存为 parks_map.html，请在浏览器中打开查看") 