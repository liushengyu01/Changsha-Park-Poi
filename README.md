# 长沙市公园及周边设施分析系统

这是一个基于Python的数据可视化项目，用于分析和展示长沙市公园及其周边设施（POI）的分布情况。项目使用高德地图API获取数据，并通过Folium库生成交互式地图可视化。

## 功能特点

- 公园分布可视化：在地图上展示长沙市主要公园的位置和基本信息
- 周边设施分析：展示公园周边的餐饮、住宿、购物、学校、文体中心、公交地铁等设施
- 热力图展示：通过热力图直观展示POI分布密度
- 交通流量分析：展示公园周边交通状况
- 交互式地图：支持缩放、平移、点击查看详细信息等交互功能

## 项目结构

```
├── visualize.py          # 主要可视化脚本
├── visualize_heatmap.py  # 热力图生成脚本
├── visualize_traffic.py  # 交通流量可视化脚本
├── circle_flow.py        # 环形流量图生成脚本
├── surround_poi.py       # 周边POI数据获取脚本
├── park.py              # 公园数据获取脚本
├── parks.csv            # 公园数据
├── parks.json           # 公园JSON格式数据
├── surrounding_pois.csv # 周边POI数据
├── traffic_status.csv   # 交通状况数据
└── *.html               # 生成的可视化地图文件
```

## 安装说明

1. 确保已安装Python 3.6或更高版本
2. 安装所需依赖：
```bash
pip install pandas folium
```

## 使用方法

1. 运行公园及周边设施可视化：
```bash
python visualize.py
```

2. 生成热力图：
```bash
python visualize_heatmap.py
```

3. 查看交通流量：
```bash
python visualize_traffic.py
```

生成的HTML文件可以直接在浏览器中打开查看交互式地图。

## 数据来源

- 公园数据：高德地图API
- POI数据：高德地图API
- 交通数据：高德地图API

## 注意事项

- 使用前请确保有稳定的网络连接
- 地图数据来源于高德地图，使用时请遵守相关使用条款
- 建议使用现代浏览器（Chrome、Firefox、Edge等）查看生成的地图

## 贡献

欢迎提交Issue和Pull Request来帮助改进项目。

## 许可证

MIT License 