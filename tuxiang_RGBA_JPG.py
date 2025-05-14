import os
from PIL import Image


def convert_images_in_folder(folder_path):
    """
    将文件夹中所有图像从 RGBA 和 P 模式转换为 RGB，并保存为 JPG 格式。
    同时检查并删除损坏的 JPG 图像。
    """
    # 获取文件夹中的所有文件
    for filename in os.listdir(folder_path):
        if filename.endswith(('.png', '.jpg', '.jpeg', '.bmp')):  # 处理常见的图像格式
            image_path = os.path.join(folder_path, filename)
            try:
                with Image.open(image_path) as img:
                    # 检查图像模式并进行转换
                    if img.mode == 'RGBA':
                        img = img.convert('RGB')
                        new_filename = os.path.splitext(filename)[0] + '.jpg'
                        new_image_path = os.path.join(folder_path, new_filename)
                        img.save(new_image_path, 'JPEG')
                        print(f'已将 {filename} 转换为 {new_filename}')

                    elif img.mode == 'P':
                        img = img.convert('RGB')
                        new_filename = os.path.splitext(filename)[0] + '.jpg'
                        new_image_path = os.path.join(folder_path, new_filename)
                        img.save(new_image_path, 'JPEG')
                        print(f'已将 {filename} 转换为 {new_filename}')

                    elif img.mode == 'RGB':
                        print(f'{filename} 已是 RGB 模式，无需转换。')

            except Exception as e:
                print(f'无法处理 {filename}，错误信息：{e}')
                if filename.lower().endswith('.jpg'):
                    # 删除损坏的 JPG 图像
                    os.remove(image_path)
                    print(f'已删除损坏的 JPG 图像：{filename}')


def remove_broken_jpgs(folder_path):
    """
    检查并删除文件夹中的损坏 JPG 图像。
    """
    for filename in os.listdir(folder_path):
        if filename.lower().endswith('.jpg'):
            image_path = os.path.join(folder_path, filename)
            try:
                with Image.open(image_path) as img:
                    img.verify()  # 验证图像文件的完整性
            except Exception as e:
                print(f'损坏的 JPG 图像：{filename}，错误信息：{e}')
                os.remove(image_path)  # 删除损坏的 JPG 图像
                print(f'已删除损坏的 JPG 图像：{filename}')


if __name__ == '__main__':
    folder_path = r"C:\Users\userone\Desktop\sougou"

    # 首先删除损坏的 JPG 图像
    remove_broken_jpgs(folder_path)

    # 然后转换图像
    convert_images_in_folder(folder_path)
