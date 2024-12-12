import openpyxl
import urllib3

# 禁用所有警告
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
def down_load(url,path):
    import requests

    headers = {
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "accept-language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
        "priority": "u=0, i",
        "referer": "https://subhd.tv/",
        "sec-ch-ua": "\"Microsoft Edge\";v=\"131\", \"Chromium\";v=\"131\", \"Not_A Brand\";v=\"24\"",
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "\"Windows\"",
        "sec-fetch-dest": "document",
        "sec-fetch-mode": "navigate",
        "sec-fetch-site": "same-site",
        "sec-fetch-user": "?1",
        "upgrade-insecure-requests": "1",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36 Edg/131.0.0.0"
    }
    response = requests.get(url, headers=headers,verify=False)
    response.close()
    with open(path, 'wb') as f:
        f.write(response.content)
workbook = openpyxl.load_workbook('电影url数据.xlsx')
sheet = workbook.active
lists = []
for row in sheet.iter_rows(values_only=True,min_row=2):
    name = row[0]
    link = row[1]
    geshi = link.split('.')[-1]
    down_load(link,f'data/{name}.{geshi}')
    print(f'------------------------{name}下载成功------------------------')
