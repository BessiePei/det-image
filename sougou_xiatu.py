import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlencode

def download_images(url, max_images, save_path):
    # 创建保存图片的文件夹
    if not os.path.exists(save_path):
        os.makedirs(save_path)

    downloaded_images = 0  # 记录已下载图片数量

    # 记录已下载图片的信息的文件路径
    record_file = os.path.join(save_path, "downloaded_images.txt")

    # 如果记录文件不存在，则创建并写入标题
    if not os.path.exists(record_file):
        with open(record_file, "w") as f:
            f.write("Downloaded Images\n")

    # 从记录文件中读取已下载的图片URL
    downloaded_urls = set()
    if os.path.exists(record_file):
        with open(record_file, "r") as f:
            for line in f:
                if line.strip() and ':' in line:
                    url = line.split(':')[1].strip()
                    downloaded_urls.add(url)

    # 循环直到达到最大图片数量或无法获取更多图片为止
    did = 0  # 从0开始进行翻页
    while downloaded_images < max_images:
        try:
            # 更新请求参数中的 did
            params['did'] = str(did)

            # 发送请求获取页面内容
            response = requests.get(url, params=params)
            html_content = response.text

            # 使用BeautifulSoup解析HTML内容
            soup = BeautifulSoup(html_content, "html.parser")

            # 找到所有图片链接所在的标签
            img_tags = soup.find_all("img", {"drag-img": True})
            img_tags.extend(soup.select("#imgArea > div.img-preview-wrap > div > div > img"))

            # 提取图片链接
            image_urls = [img["drag-img"] for img in img_tags]

            # 如果没有找到新的图片，则结束循环
            if not image_urls:
                print("未找到新的图片，结束下载。")
                break

            # 遍历图片链接，下载并保存图片
            for image_url in image_urls:
                if downloaded_images >= max_images:
                    break
                try:
                    # 解析链接，检查是否已经包含协议部分
                    if not image_url.startswith("http"):
                        image_url = "https:" + image_url

                    # 如果图片URL已经存在于已下载集合中，则跳过
                    if image_url in downloaded_urls:
                        print(f"图片 {image_url} 已存在，跳过下载！")
                        continue

                    # 保存图片到本地
                    image_name = f"image_{downloaded_images + 1}.jpg"
                    image_path = os.path.join(save_path, image_name)

                    response = requests.get(image_url, verify=False)
                    if response.status_code == 200:
                        with open(image_path, "wb") as f:
                            f.write(response.content)
                        print(f"图片 {image_name} 保存成功！")
                        downloaded_images += 1
                        downloaded_urls.add(image_url)  # 添加到已下载集合

                        # 记录已下载的图片信息到文件中
                        with open(record_file, "a") as f:
                            f.write(f"{image_name}: {image_url}\n")
                    else:
                        print(f"图片 {image_url} 下载失败！")
                except Exception as e:
                    print(f"下载图片 {image_url} 时出错: {e}")
                    continue

            did += 48  # 递增请求变量 did，以获取下一页的图片

        except Exception as e:
            print(f"请求页面 {url} 时出错: {e}")
            break

if __name__ == "__main__":
    query = "网球"  # 类别query参数
    base_url = "https://pic.sogou.com/d?"
    params = {
        "query": query,
        "forbidqc": "",
        "entityid": "",
        "preQuery": "",
        "rawQuery": "",
        "queryList": "",
        "st": "",
        "mode": "13",
        "cwidth": "1920",
        "cheight": "1080",
        "dm": "4",
        "did": "0"  # 初始设置为 0
    }
    max_images = 5000  # 最大图片数量
    save_path = r"C:\Users\userone\Desktop\wangqiu"  # 保存路径
    url = base_url + urlencode(params)
    download_images(url, max_images, save_path)