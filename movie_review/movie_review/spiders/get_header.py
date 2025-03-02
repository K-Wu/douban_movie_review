from __future__ import annotations
# 获取登陆后浏览器header，用以爬取登陆后才能看到的内容
# Adapted from https://github.com/7325156/jjwxcNovelCrawler/blob/master/client.py

from selenium import webdriver
# import time
# from selenium.webdriver.common.by import By

def _get_douban_headers() -> dict[str, str]:
    #此处需要安装chormedriver ，并存放到python路径下
    driver=webdriver.Edge()

    driver.delete_all_cookies()
    driver.get("https://accounts.douban.com/passport/login?source=book")


    input("请在浏览器中登陆后，按回车键继续...")

    cookies = driver.get_cookies()
    cookies_list= []
    for cookie_dict in cookies:
        cookie =cookie_dict['name']+'='+cookie_dict['value']
        cookies_list.append(cookie)
    header_cookie = ';'.join(cookies_list)
    
    headers = {
        'cookie':header_cookie,
        'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36'
    }

    # print(headers)
    driver.quit()
    return headers

__GLOBAL_DOUBAN_HEADERS = None

def get_douban_headers() -> dict[str, str]:
    global __GLOBAL_DOUBAN_HEADERS
    if __GLOBAL_DOUBAN_HEADERS is None:
        __GLOBAL_DOUBAN_HEADERS = _get_douban_headers()
    return __GLOBAL_DOUBAN_HEADERS