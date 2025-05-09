import requests
import json
import time
import csv
from typing import Dict, List

# 读取公园数据
with open('parks.json', 'r', encoding='utf-8') as f:
    parks_data = json.load(f)

# API配置
key = "54fa79c7e77e9832ae19b77830ffe75d"  # 使用你的高德地图API Key
radius = 1000  # 搜索半径，单位：米

# POI类型代码
poi_types = {
    "餐饮": "050000",  # 餐饮服务
    "住宿": "100000",  # 住宿服务
    "购物": "060000",  # 购物服务
    "学校": "141200",  # 学校
    "文体中心": "080000",  # 体育休闲服务
    "公交地铁": "150000"  # 交通设施服务
}

def search_surrounding_pois(location: str, poi_type: str) -> List[Dict]:
    """搜索指定位置周边的POI"""
    url = f"https://restapi.amap.com/v3/place/around"
    params = {
        "key": key,
        "location": location,
        "radius": radius,
        "types": poi_type,
        "offset": 100,  # 每页记录数
        "page": 1,     # 页码
        "extensions": "all"
    }
    
    try:
        response = requests.get(url, params=params)
        data = response.json()
        if data["status"] == "1" and "pois" in data:
            return data["pois"]
        return []
    except Exception as e:
        print(f"搜索POI时出错: {e}")
        return []

def main():
    # 存储所有结果
    all_results = []
    
    # 遍历每个公园
    for park in parks_data["pois"]:
        park_name = park["name"]
        location = park["location"]
        
        print(f"正在处理公园: {park_name}")
        
        # 对每种POI类型进行搜索
        for poi_category, poi_type in poi_types.items():
            print(f"  搜索{poi_category}...")
            pois = search_surrounding_pois(location, poi_type)
            
            # 处理搜索结果
            for poi in pois:
                result = {
                    "公园名称": park_name,
                    "公园位置": location,
                    "POI类别": poi_category,
                    "POI名称": poi.get("name", ""),
                    "POI地址": poi.get("address", ""),
                    "POI位置": poi.get("location", ""),
                    "POI电话": poi.get("tel", ""),
                    "POI评分": poi.get("biz_ext", {}).get("rating", ""),
                    "POI距离": poi.get("distance", "")
                }
                all_results.append(result)
            
            # 添加延迟，避免请求过于频繁
            time.sleep(0.5)
    
    # 保存为CSV文件
    if all_results:
        with open('surrounding_pois.csv', 'w', encoding='utf-8-sig', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=all_results[0].keys())
            writer.writeheader()
            writer.writerows(all_results)
        print("数据已保存到 surrounding_pois.csv")
    else:
        print("没有找到任何POI数据")

if __name__ == "__main__":
    main()
