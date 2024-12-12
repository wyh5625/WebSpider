import os
import subprocess

import pandas as pd
from DrissionPage import ChromiumPage, ChromiumOptions
import time
from switch_ips import fetch_ips, switch_ip, get_extension_options
import signal
import sys

page_on = 2083

co = get_extension_options()
page = ChromiumPage(co)

config_id = 0

# List of .ovpn configuration files
configs = [
    #"US-1.ovpn", # 45.134.142.69
    "US-2.ovpn", # 185.220.69.105
    "US-3.ovpn", # 217.148.140.136
    "US-4.ovpn", # 149.102.243.8
    "US-5.ovpn", # 149.88.25.212
    "US-6.ovpn", # 185.220.69.105
    "US-7.ovpn", # 169.150.205.135
    "US-8.ovpn", # 64.31.20.21
    "US-9.ovpn", # 107.175.196.105
    "US-10.ovpn", # 192.3.53.230
]

vpn_process = None  # Variable to hold the VPN process

def run_vpn(config_path):
    global vpn_process
    if vpn_process is not None:
        # Terminate the previous VPN process if it exists
        vpn_process.terminate()
        vpn_process.wait()  # Wait for the process to terminate

    command = [
        "sudo", "openvpn",
        "--config", config_path,
        "--auth-user-pass", "credentials.txt",
        # "--daemon"
    ]

    vpn_process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

    # Read output and error streams
    for line in vpn_process.stdout:
        print(line.strip())

    return vpn_process

def add_default_route():
    # Command to add the default route
    command = ["sudo", "route", "add", "default", "192.168.0.1"]

    try:
        # Execute the command
        subprocess.run(command, check=True)
        print("Default route added successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Error adding default route: {e}")

def terminate_vpn(signum, frame):
    if vpn_process is not None:
        vpn_process.terminate()
        vpn_process.wait()  # Ensure the process has terminated

        add_default_route()

    print("VPN process terminated. Exiting script.")
    sys.exit(0)

# Set up signal handling
signal.signal(signal.SIGINT, terminate_vpn)
signal.signal(signal.SIGTERM, terminate_vpn)

while True:
    # Create a page instance
    web_url = "https://subhd.tv/sub/tv/" + str(page_on)

    page.get(web_url)

    # Locate the block by class (adjust the class as needed)
    movie_blocks = page.eles('xpath://div[contains(@class, "col-lg-10")]//div[contains(@class, "clearfix")]')

    # Iterate through each block to find the desired <a> element
    new_movies = []
    for block in movie_blocks:
        # Use relative XPath to locate the <a> within the block
        a_element = block.ele('xpath:.//a[@class="link-dark align-middle"]')
        title = a_element.text
        subtitle = block.ele('xpath:.//a[@class="link-dark"]')
        tag = block.ele('xpath:.//div[contains(@class, "text-truncate py-2 f11")]')

        # print("Title: ", a_element.text)
        # print("Subtitle: ", subtitle.text)
        # print("Annotation tags: ", tag.text)

        movie = {
            "title": a_element.text,
            "subtitle": subtitle.text,
            "tag": tag.text,
            "url": a_element.attr('href'),
        }
        new_movies.append(movie)
    # print(new_movies)
    if new_movies:

        # File path for the Excel file
        excel_file_path = 'movies.xlsx'
        # Check if the Excel file exists
        if os.path.exists(excel_file_path):
            # Read the existing movies from the Excel file
            existing_df = pd.read_excel(excel_file_path, engine='openpyxl')
        else:
            # Create an empty DataFrame if the file does not exist
            existing_df = pd.DataFrame(columns=["title", "subtitle", "tag", "url"])

        # Convert new movies to a DataFrame
        new_df = pd.DataFrame(new_movies)

        # Check for duplicates based on the title
        combined_df = pd.concat([existing_df, new_df])
        combined_df = combined_df.drop_duplicates(subset=["title"], keep='first')

        # Write the updated DataFrame back to the Excel file
        combined_df.to_excel(excel_file_path, index=False)

        print(f"Movies on page: {page_on}, written to {excel_file_path}, with duplicates removed.")
        # switch_ip(page, f"{ip_all[next_id]['ip']}:{ip_all[next_id]['port']}")
        # page.get("https://www.ip138.com/", retry=0)
        # time.sleep(10)
        # next_id += 1

        page_on += 1

    else:
        error = page.ele('Internal Server Error')
        if error:
            page_on += 1
        else:
            print(f"No movies on page: {page_on}, exceed the maximum page!")
            print(f"IP is blocked, run the vpn!")
            vpn_process = run_vpn(configs[config_id])
            config_id = (config_id + 1)%len(configs)
            time.sleep(10)  # Wait for the VPN to establish
            
        # switch_ip(page, f"{ip_all[next_id]['ip']}:{ip_all[next_id]['port']}")
        # page.get("https://www.ip138.com/", retry=0)
        # next_id += 1
        # break

# movies[0]["link"].click()


# 获取背景图像的 URL
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


# for track in tracks:
#             ac.move(offset_x=track, offset_y=random.uniform(-7.5, 10.5), duration=random.uniform(0.3, 0.8))
#             sleep(random.uniform(0.01, 0.04))

