import requests
import pandas as pd
import time


def get_traffic_status(location, park_name, api_key, radius=1000):
    output_format = "json"
    extensions = "all"
    url = f"https://restapi.amap.com/v3/traffic/status/circle?location={location}&radius={radius}&output={output_format}&extensions={extensions}&key={api_key}"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            data['park_name'] = park_name
            data['location'] = location
            return data
        else:
            print(f"请求失败，状态码: {response.status_code}, 公园: {park_name}")
            return {'park_name': park_name, 'location': location, 'error': f'status_code_{response.status_code}'}
    except requests.RequestException as e:
        print(f"请求过程中出现错误: {e}, 公园: {park_name}")
        return {'park_name': park_name, 'location': location, 'error': str(e)}


def main():
    api_key = "54fa79c7e77e9832ae19b77830ffe75d"
    parks_df = pd.read_csv('parks.csv')
    results = []
    for idx, row in parks_df.iterrows():
        location = row['location']
        park_name = row['name']
        data = get_traffic_status(location, park_name, api_key)
        results.append(data)
        time.sleep(0.5)  # 防止请求过快被限流
    # 只保留主要字段，展开 trafficinfo 字段
    records = []
    for item in results:
        base = {'park_name': item.get('park_name'), 'location': item.get('location')}
        if 'trafficinfo' in item:
            trafficinfo = item['trafficinfo']
            for k, v in trafficinfo.items():
                base[k] = v
        else:
            base['error'] = item.get('error', 'no trafficinfo')
        records.append(base)
    df = pd.DataFrame(records)
    df.to_csv('traffic_status.csv', index=False, encoding='utf-8-sig')
    print('已保存至 traffic_status.csv')

if __name__ == "__main__":
    main()