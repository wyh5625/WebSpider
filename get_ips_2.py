import requests

def get_ip():
    # 设置参数
    url = "https://api.xiaoxiangdaili.com/ip/get"
    params = {
        "appKey": "1183860027531087872",          # 替换为你的appKey
        "appSecret": "23lgacNo",     # 替换为你的appSecret
        "cnt": 1,                        # 可选，提取数量
        "wt": "json",                    # 可选，响应体格式
        "method": "http",                # 可选，代理方式
        "releaseAuto": 1                 # 可选，仅长效IP应用下有效
    }

    # 发送请求
    response = requests.get(url, params=params)

    # 处理响应
    if response.status_code == 200:
        data = response.json()
        print(data)
        return data['data'][0]['ip'], data['data'][0]['port']
    else:
        print(f"请求失败，状态码: {response.status_code}, 消息: {response.text}")
