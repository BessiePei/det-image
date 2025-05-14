# -*- coding: utf-8 -*-
"""
@Time ： 2023/4/25 9:24
@Auth ： RS迷途小书童
@File ：Get_image_online.py
@IDE ：PyCharm
@Purpose: 批量获取网页上的图片制作数据集
"""
import requests
import re
from urllib import error
import urllib3
import time
import os

urllib3.disable_warnings()


def Get_image_url(headers, key, num):
    """
    :param headers: 请求头
    :param key: 输入搜索的关键字
    :param num: 输入图片数量
    :return: 列表形式的下载链接
    """


    page_all = 0
    page_image = 0
    page_sum = int(num / 60) + 1
    image_urls = []
    while page_image <= page_sum:
        print("正在获取第%s页图片下载链接......" % (page_image + 1))
        url = 'https://image.baidu.com/search/flip?tn=baiduimage&ie=utf-8&word=' + str(key) + '&pn=%s' % page_all
        request = requests.get(url, headers=headers, timeout=10, allow_redirects=False, verify=False)
        # timeout实现网页未返回值的情况 # 获取网页的代码
        image_urls_page = re.findall('"objURL":"(.*?)",', request.text, re.S)
        if not image_urls_page:
            print("Error:第%s页图片下载链接获取失败！" % (page_image + 1) + "错误链接：" + url)
            num = page_image * 60 - 40
            print("当前共有%s张图片" % num)
            break
        else:
            image_urls += image_urls_page
            # 获取图片的下载链接，列表形式
            page_image += 1
        page_all += 60
    return image_urls


def Write_image(image_urls, num, path, header):
    """
    :param image_urls: 以列表的形式输入下载链接
    :param num: 输入图片数量
    :param path: 输入存储路径
    :param header: 请求头文件
    :return: none,保存本地
    """
    print("开始下载目标图片")
    num_image = 0
    num_all = 0
    if not os.path.exists(path):
        os.makedirs(path)
    while num_image < num:
        try:
            if image_urls[num_image] is not None:
                image_data = requests.get(image_urls[num_all], headers=header, verify=False, timeout=4)
                # 获取下载链接中的图片信息
                print("正在下载第%s张图片" % (num_image + 1) + ",下载链接:" + image_urls[num_all])
                image_path = os.path.join(path, str(num_image + 1) + ".jpg")
                with open(image_path, 'wb') as fp:
                    fp.write(image_data.content)
                    # 写入图片信息
                    num_image += 1
                    num_all += 1
            else:
                num_all += 1
                continue
        except BaseException:
            print('Error:当前图片下载失败，下载链接：%s' % image_urls[num_all])
            num_all += 1
            continue


if __name__ == '__main__':
    headers1 = {
        'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
        'Connection': 'keep-alive',
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:60.0) Gecko/20100101 Firefox/60.0',
        'Upgrade-Insecure-Requests': '1'
    }
    # key1 = str(input("请输入你想要获取图片的关键字："))
    # num1 = int(input("请输入你想获取图片的数量："))
    # 爬虫图像需要的信息（需要修改）
    key1 = "网球"
    num1 = 5000
    path1 = r"C:\Users\userone\Desktop\wangqiu\\" #下载路径

    start = time.perf_counter()
    image_urls1 = Get_image_url(headers1, key1, num1)
    if image_urls1:
        Write_image(image_urls1, num1, path1, headers1)
    else:
        print("Error:程序结束！")
    end = time.perf_counter()
    print("\n")
    print("图片全部下载完成......")
    print('共消耗: %s 秒' % (end - start))
