import base64

import requests
from DrissionPage import ChromiumPage
import time

def download(url):
    page = ChromiumPage()
    page.get(url)
    page.wait.load_start()
    download_btn = page.ele('t:button@tx():下载字幕文件')
    time.sleep(2)
    download_btn.click()
    time.sleep(5)
    page.wait.load_start()

    # 定位到 base64 图像
    img_element = page.ele('xpath://img[@class="tc-bg-placeholder"]')

    if img_element:
        # 获取 base64 数据
        img_src = img_element.get_attribute('src')
        if img_src.startswith('data:image/png;base64,'):
            # 提取 base64 字符串并解码
            img_data = img_src.split(',')[1]
            img_data = base64.b64decode(img_data)  # 解码 base64 数据

            # 保存为 PNG 文件
            with open('placeholder_image.png', 'wb') as file:
                file.write(img_data)
            print("Base64 image saved as placeholder_image.png")
    else:
        print("Base64 image not found.")

    # 定位到背景图像的 URL
    bg_element = page.ele('xpath://div[@id="slideBg"]')
    if bg_element:
        # 获取背景图像的 CSS 样式
        bg_style = bg_element.get_attribute('style')
        # 提取背景图像的 URL
        bg_image_url = bg_style.split('url("')[1].split('")')[0]

        # 下载背景图像
        response = requests.get(bg_image_url)
        if response.status_code == 200:
            with open('background_image.png', 'wb') as file:
                file.write(response.content)
            print("Background image saved as background_image.png")
        else:
            print("Failed to download background image.")
    else:
        print("Background image not found.")

    # # 获取背景图像的 URL
    # bg_image_url = page.ele('xpath://div[@id="slideBg"]').get_attribute('style')
    # # 提取 URL
    # bg_image_url = bg_image_url.split('url("')[1].split('")')[0]
    #
    # page.download(bg_image_url, '.', 'img')

    # # 下载图像
    # response = requests.get(bg_image_url)
    #
    # # 保存图像到本地文件
    # with open('background_image.png', 'wb') as file:
    #     file.write(response.content)
    #
    # print("图像已保存为 background_image.png")




web_url = "https://subhd.tv/a/576124"
download(web_url)