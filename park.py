import requests
import json
import csv

# 定义要搜索的公园列表
parks = [
    "浏阳河婚庆公园",
    "桂花公园",
    "五一广场",
    "红星社区公园",
    "海棠公园",
    "望月公园",
    "八方公园",
    "紫凤公园",
    "晓园公园",
    "金峰公园"
]

# API配置
city = "长沙"
key = "54fa79c7e77e9832ae19b77830ffe75d"
extensions = "all"

# 存储所有结果
all_results = []

# 遍历每个公园进行搜索
for park_name in parks:
# 构建请求URL
    url = f"https://restapi.amap.com/v3/place/text?keywords={park_name}&city={city}&key={key}&extensions={extensions}"

headers = {
    'Content-Type': 'application/json'
}

# 发起GET请求
response = requests.request("GET", url, headers=headers)
data = response.json()

# 如果搜索成功且有结果
if data["status"] == "1" and "pois" in data and data["pois"]:
    # 只取第一条结果
    first_result = data["pois"][0]
    all_results.append(first_result)
    print(f"已找到公园: {park_name}")
else:
    print(f"未找到公园: {park_name}")

# 保存为JSON文件
with open('parks.json', 'w', encoding='utf-8') as json_file:
    json.dump({"pois": all_results}, json_file, ensure_ascii=False, indent=4)

# 保存为CSV文件
if all_results:
    with open('parks.csv', 'w', encoding='utf-8-sig', newline='') as csv_file:
        # 获取所有可能的字段
        fieldnames = set()
        for poi in all_results:
            fieldnames.update(poi.keys())
        
        # 创建CSV写入器
        writer = csv.DictWriter(csv_file, fieldnames=sorted(fieldnames))
        writer.writeheader()
        
        # 写入数据
        for poi in all_results:
            writer.writerow(poi)

print(f"数据已保存为 parks.json 和 parks.csv，共找到 {len(all_results)} 个公园")


