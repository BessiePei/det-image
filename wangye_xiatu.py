import os
import requests
from bs4 import BeautifulSoup
from PIL import Image
from io import BytesIO

def download_images(url, save_folder, max_images=100):
    if not os.path.exists(save_folder):
        os.makedirs(save_folder)

    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    images = soup.find_all('img', limit=max_images)

    downloaded_count = 0

    for img in images:
        img_url = img.get('data-src') or img.get('src')
        if not img_url:
            continue

        # 检查并修正URL
        if img_url.startswith('//'):
            img_url = 'https:' + img_url
        elif not img_url.startswith('http'):
            print(f"无效的URL，跳过: {img_url}")
            continue

        try:
            img_data = requests.get(img_url, timeout=5)
            img_data.raise_for_status()  # Check for HTTP errors

            # Convert to JPG if the image is in a different format
            with Image.open(BytesIO(img_data.content)) as img:
                # Convert image to RGB or RGBA based on its mode
                if img.mode == 'P':
                    img = img.convert('RGBA')
                img = img.convert('RGB')  # Ensure it's RGB before saving

                img_name = os.path.join(save_folder, f'image_{downloaded_count + 1}.jpg')
                img.save(img_name, 'JPEG')
                downloaded_count += 1
                print(f"Downloaded: {img_name}")

                if downloaded_count >= max_images:
                    break

        except Exception as e:
            print(f"下载失败: {img_url}, 错误信息：{e}")
            continue

if __name__ == '__main__':
    url = 'https://pic.sogou.com/pics?query=%E7%BD%91%E7%90%83'
    save_folder = r"C:\Users\userone\Desktop\wangqiu"
    download_images(url, save_folder, max_images=100)
