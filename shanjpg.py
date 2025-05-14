#删除没有json文件的jpg(打标签后，挑出有标签的用于训练）
from PIL import Image
import os
import time

start = time.time()
n = 0
# 指明被遍历的文件夹
rootdir = r'C:\Users\userone\Desktop\tennis_jpg\sougou_512x512'  # 图片路径

# 获取所有的 JSON 文件名（不包括扩展名）
json_files = {os.path.splitext(f)[0] for f in os.listdir(rootdir) if f.endswith('.json')}

for parent, dirnames, filenames in os.walk(rootdir):
    # 遍历每一个文件
    for filename in filenames:
        currentPath = os.path.join(parent, filename)  # 当前文件的路径
        picture_number, extension = os.path.splitext(filename)  # 分离文件名和扩展名
        print("the file name is:" + filename)

        # 检查文件是否为 JPG 文件且没有对应的 JSON 文件
        if extension.lower() == '.jpg' and picture_number not in json_files:
            print("Deleting:", currentPath)
            os.remove(currentPath)  # 删除没有对应 JSON 文件的 JPG 文件
            n += 1

end = time.time()
print("Execution Time:", end - start)
print("删除的照片数为：", n)
