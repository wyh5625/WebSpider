import platform
import time

import requests
from DrissionPage import ChromiumPage, ChromiumOptions
from loguru import logger
from selenium.webdriver.common.keys import Keys

from get_ips import extract_ips_from_file

def get_extension_options():
    co = ChromiumOptions()
    # co.headless(True)  # 设置无头加载  无头模式是一种在浏览器没有界面的情况下运行的模式，它可以提高浏览器的性能和加载速
    # co.incognito(True)  # 无痕隐身模式打开的话，不会记住你的网站账号密码的
    # co.set_argument(
    #     '--no-sandbox')  # 禁用沙箱 禁用沙箱可以避免浏览器在加载页面时进行安全检查,从而提高加载速度 默认情况下，所有Chrome 用户都启用了隐私沙盒选项  https://zhuanlan.zhihu.com/p/475639754
    co.set_argument("--disable-gpu")  # 禁用GPU加速可以避免浏览器在加载页面时使用过多的计算资源，从而提高加载速度
    # co.set_user_agent(user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36')  # 设置ua
    # co.set_timeouts(6, 6, 6)
    co.set_local_port(9211)
    # 1、设置switchyOmega插件
    # co.add_extension(r'./proxy_switchyomega-2.5.20-an+fx')

    return co

def get_free_ip(browser):
    # url = "https://www.zdaye.com/free/?ip=&adr=&checktime=&sleep=&cunhuo=&dengji=1&nadr=&https=&yys=&post=&px="
    url = "https://ip.ihuan.me"
    browser.get(url, retry=3, interval=1, timeout=15)
    ip_ports = []
    # for tr in browser.eles('x://table[@id="ipc"]//tr')[1:]:
    tb = browser.ele('x://table[@class="table table-hover table-bordered"]/tbody')
    for tr in tb.eles('x:/tr')[1:]:
        tds = [td.text for td in tr.eles("x:/td")]
        ip = {
            "ip": tds[0],
            "port": tds[1],
            "addr": tds[2]
        }
        ip_ports.append(ip)
    print(len(ip_ports), ip_ports)
    return ip_ports

# API URL
API_URL = "http://api.shenlongproxy.com/ip?cty=00&c=10&pt=1&ft=txt&pat=\\n&rep=1&key=1c0a975f&ts=20"

def fetch_ips():
    try:
        # 发送 GET 请求到 API
        response = requests.get(API_URL)

        # 检查请求是否成功
        response.raise_for_status()

        # 获取返回的内容
        ip_data = response.text

        # 按行分割并提取 IP 地址
        ips = ip_data.strip().split('\n')

        return ips

    except requests.exceptions.RequestException as e:
        print(f"请求出现错误: {e}")
        return []

def switch_ip(browser, ip_port=None):
    global set_proxy
    omega_proxy = False
    if ip_port:
        # 设置proxy
        ip, port = ip_port.split(":")
        tab = browser.new_tab()
        tab.get("chrome-extension://padekgcemlokbadohgkifijomclgjgif/options.html#!/profile/proxy")

        input_host = tab.ele('xpath://input[@ng-model="proxyEditors[scheme].host"]')
        input_host.clear(by_js=True)
        input_port = tab.ele('xpath://input[@ng-model="proxyEditors[scheme].port"]')
        input_port.clear(by_js=True)

        input_host.input(ip, clear=True)
        input_port.input(port, clear=True)
        tab.ele('x://a[@ng-click="applyOptions()"]').click()
        # tab.wait(1000)
        # 提示框
        txt = tab.handle_alert()
        print("提示框", txt)
        tab.handle_alert(accept=False)
        if not omega_proxy:
            # 切换proxy
            tab.get("chrome-extension://padekgcemlokbadohgkifijomclgjgif/popup/index.html#")
            tab.wait(1)
            tab.ele('x://span[text()="proxy"]').click()
            set_proxy = True
    else:
        tab = browser.new_tab()
        tab.get("chrome-extension://padekgcemlokbadohgkifijomclgjgif/popup/index.html#")
        tab.ele('x://span[text()="[直接连接]"]').click()
    if len(browser.tab_ids) > 1:
        print("当前tab个数", len(browser.tab_ids))
        try:
            tab.close()
        except Exception as e:
            logger.warning("Attempted to close a tab that was already disconnected.", e)

if __name__ == "__main__":
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
    # ip_file = "ip_list.txt"
    # ip_all = extract_ips_from_file(ip_file)
    print(ip_all)
    # ip_all = [{"ip": "10.1.3.56", "port": 7890, "expire_time": "2025-04-27 22:24:00"}]
    for ips in ip_all:
        logger.info(f"~~~切换ip，now {ips['ip']}")
        # 重置switchyOmega插件
        switch_ip(browser, f"{ips['ip']}:{ips['port']}")
        browser.wait(1)
        try:
            browser.get("https://www.baidu.com/", retry=0)
            time.sleep(10)
            browser.get("https://subhd.tv/sub/tv/789", retry=0)
            # browser.get("https://www.ip138.com/", retry=0)
            browser.get("https://www.google.com/", retry=0)
            browser.get("https://whoer.net/zh", retry=0)
            html_text = browser.ele('x://div[@class="button_icon your-ip"]').text
            logger.success(f">>>>>>>>切换代理成功 {html_text}")
        except Exception as err:
            logger.error(f"----------切换代理失败 dp {err}")
        browser.wait(10)
    # browser.quit()
    # browser.quit()