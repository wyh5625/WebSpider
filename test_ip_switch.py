from get_ips import extract_ips_from_file
from switch_ips import fetch_ips, switch_ip, get_free_ip, get_extension_options
from DrissionPage import ChromiumPage, ChromiumOptions
from loguru import logger
import platform

# # address_list = fetch_ips()
# address_list = get_free_ip()
# print(address_list)
# for addr in address_list:
#     # ip, port = addr.split(":")
#     # switch_ip(addr)
#     switch_ip(f"{addr['ip']}:{addr['port']}")

co = get_extension_options()
browser = ChromiumPage(co)

# 2、重置switchyOmega插件
omega_proxy = False
switch_ip(browser)
browser.get("https://www.ip138.com/", retry=0)
# html_text = browser.get_frame('x://div[@class="hd"]//iframe').ele('text:您的iP地址是').text
# logger.success(f">>>>当前的ip {html_text}")

# 3、随机切换代理ip
ip_all = get_free_ip(browser)
# ip_all = [{"ip": "10.1.3.56", "port": 7890, "expire_time": "2025-04-27 22:24:00"}]
# ip_file = "ip_list.txt"
# ip_all = extract_ips_from_file(ip_file)
print(ip_all)

for ips in ip_all:
    logger.info(f"~~~切换ip，now {ips['ip']}")
    # 重置switchyOmega插件
    switch_ip(browser, f"{ips['ip']}:{ips['port']}")
    browser.wait(1)
    try:
        browser.get("https://www.baidu.com/", retry=0)
        browser.get("https://www.ip138.com/", retry=0)
        browser.get("https://www.google.com/", retry=0)
        browser.get("https://www.ip138.com/", retry=0)
        html_text = browser.get_frame('x://div[@class="hd"]//iframe').ele('text:您的iP地址是').text
        logger.success(f">>>>>>>>切换代理成功 {html_text}")
    except Exception as err:
        logger.error(f"----------切换代理失败 dp {err}")
    browser.wait(10)