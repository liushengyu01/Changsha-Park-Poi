import pandas as pd
import folium
import ast

# 读取交通态势数据
traffic_df = pd.read_csv('traffic_status.csv')

# 交通状况与颜色映射
status_color = {
    1: 'green',   # 畅通
    2: 'orange',  # 缓慢
    3: 'red',     # 拥堵
    0: 'gray',    # 未知
    '未知': 'gray'
}

status_text = {
    1: '畅通',
    2: '缓慢',
    3: '拥堵',
    0: '未知'
}

def get_status_color(status):
    return status_color.get(status, 'gray')

def get_status_text(status):
    return status_text.get(status, '未知')

# 创建地图
m = folium.Map(location=[28.2, 112.98], zoom_start=12, 
               tiles='https://webrd01.is.autonavi.com/appmaptile?lang=zh_cn&size=1&scale=1&style=7&x={x}&y={y}&z={z}',
               attr='高德地图')

for idx, row in traffic_df.iterrows():
    try:
        lon, lat = map(float, str(row['location']).split(','))
        desc = row.get('description', '')
        # 公园圆点
        folium.CircleMarker(
            location=[lat, lon],
            radius=12,
            color='blue',
            fill=True,
            fill_color='blue',
            fill_opacity=0.5,
            popup=folium.Popup(f"<b>{row['park_name']}</b><br>交通状况: {desc if pd.notna(desc) else '无数据'}", max_width=300),
            tooltip=row['park_name']
        ).add_to(m)
        # 画每条道路
        if pd.notna(row.get('roads')) and str(row['roads']).startswith('['):
            try:
                roads = ast.literal_eval(row['roads'])
                for road in roads:
                    # polyline 字符串转为坐标点
                    if 'polyline' in road and road['polyline']:
                        points = [list(map(float, p.split(','))) for p in road['polyline'].split(';') if ',' in p]
                        # status 可能为字符串，转为int
                        try:
                            status = int(road.get('status', 0))
                        except:
                            status = 0
                        color = get_status_color(status)
                        text = get_status_text(status)
                        popup_html = f"""
                        <b>道路: {road.get('name','')}</b><br>
                        状态: {text}<br>
                        速度: {road.get('speed','--')} km/h<br>
                        方向: {road.get('direction','--')}<br>
                        """
                        folium.PolyLine(
                            locations=[[pt[1], pt[0]] for pt in points],
                            color=color,
                            weight=6,
                            opacity=0.8,
                            popup=folium.Popup(popup_html, max_width=300),
                            tooltip=f"{road.get('name','')}({text})"
                        ).add_to(m)
            except Exception as e:
                print(f"解析道路信息出错: {e}")
    except Exception as e:
        print(f"处理 {row['park_name']} 时出错: {e}")

# 添加图例
legend_html = '''
<div style="position: fixed; bottom: 20px; right: 20px; width: 180px; height: auto; 
            background-color: white; border:2px solid grey; z-index:9999;
            padding: 10px; font-family: Arial, sans-serif; font-size: 12px;
            border-radius: 5px; box-shadow: 0 0 10px rgba(0,0,0,0.2);">
    <b>交通状况图例</b><br>
    <span style='color:green;'>━</span> 畅通<br>
    <span style='color:orange;'>━</span> 缓慢<br>
    <span style='color:red;'>━</span> 拥堵<br>
    <span style='color:gray;'>━</span> 未知/无数据<br>
    <span style='color:blue;'>●</span> 公园位置<br>
</div>
'''
m.get_root().html.add_child(folium.Element(legend_html))

# 添加标题
title_html = '''
<div style="position: fixed; top: 20px; left: 50%; transform: translateX(-50%);
            background-color: white; border:2px solid grey; z-index:9999;
            padding: 10px; font-family: Arial, sans-serif; font-size: 16px;
            border-radius: 5px; box-shadow: 0 0 10px rgba(0,0,0,0.2);">
    <b>长沙市10大公园交通态势分布图（含道路分布）</b>
</div>
'''
m.get_root().html.add_child(folium.Element(title_html))

m.save('traffic_map.html')
print('已保存为 traffic_map.html，请在浏览器中打开查看')
