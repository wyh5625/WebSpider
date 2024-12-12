import requests
from PIL import Image
from io import BytesIO

def download_img(image_url):
# 图片 URL
# image_url = "https://t.captcha.qq.com/cap_union_new_getcapbysig?img_index=1&image=02bd27000000004a0000000ba871f7342cef&sess=s0W3j5i1aln8i-td3YBaPkK2YNlMv1Abnj48eSuLktOYrVYXYksc3B2Zd857BUeYB3R2KIAJG9ujEWynvOZ4jTiermYKKcLTPDUHbjRMo8vjtmng5MESlIWo9x14besKr2VALNOVsMPWYKjoeRNYJ7e7ML_s64_o-4ifg20_O_XbgHItMJ-Abmp7Rgg-X9MuWgEiyIyhapEDFrzMgsPQu2vSMmoeaK_itRYf2y55CgkfI2p6TJzuRcZhTFHdCa2GLYLwy8-PE5_42BkbZxxenr2_gd3dSI9sOuQL9BZsdkxy-BR7E30BsBbRVyO_ipHDEE2JRXmitlMn5qzGMUGOPLpOdzIBQ9g0A_Jqtr_6BEOjr6xExHvU4dzFP4lM_zXvs954OAXb_P1Io*&quot;"

# 发送请求获取图片
    response = requests.get(image_url)

    if response.status_code == 200:
        # 打开图片并保存
        img = Image.open(BytesIO(response.content))
        img.save("captcha.png")
        print("图片已保存为 captcha.png")
        return img
    else:
        print("无法下载图片，状态码:", response.status_code)
        return None