#VOC2coco txt ,train val 无test，分到两个文件夹
import os
import random
import shutil
import xml.etree.ElementTree as ET

# 设置VOC数据集文件夹路径
voc_dir = r'C:\Users\userone\Desktop\yolov7_tennis\VOCdevkit\VOC2007'  # 源文件名
output_dir = r'C:\Users\userone\Desktop\yolov7_tennis\VOCdevkit\VOC2007\coco'  # 目标文件名

# 创建YOLO格式的文件夹结构
yolo_subdirs = ['images/train', 'images/val', 'labels/train', 'labels/val']
for subdir in yolo_subdirs:
    os.makedirs(os.path.join(output_dir, subdir), exist_ok=True)

# 获取所有图片文件的文件名（不包括文件扩展名）
image_files = [os.path.splitext(file)[0] for file in os.listdir(os.path.join(voc_dir, 'JPEGImages'))]

# 随机打乱图片文件顺序
random.shuffle(image_files)

# 划分数据集比例（7:3）
total_images = len(image_files)
train_ratio = 0.7
val_ratio = 0.3

train_split = int(total_images * train_ratio)

# 分割数据集
train_images = image_files[:train_split]
val_images = image_files[train_split:]

# 复制图片文件到YOLO格式文件夹
def copy_images(image_list, subset):
    for image_name in image_list:
        image_path_src = os.path.join(voc_dir, 'JPEGImages', image_name + '.jpg')
        image_path_dest = os.path.join(output_dir, 'images', subset, image_name + '.jpg')
        os.makedirs(os.path.dirname(image_path_dest), exist_ok=True)  # 确保目录存在
        shutil.copy(image_path_src, image_path_dest)

copy_images(train_images, 'train')
copy_images(val_images, 'val')

class_to_idx = {
    'catheter': 0,
    'guidewire': 1,
    'spring': 2,
    # 如果你的数据集有更多类别，请继续添加映射
}

# 转换XML标签为YOLO格式并保存为txt文件
def convert_voc_to_yolo_label(image_list, subset):
    for image_name in image_list:
        label_path_src = os.path.join(voc_dir, 'Annotations', image_name + '.xml')
        label_path_dest = os.path.join(output_dir, 'labels', subset, image_name + '.txt')
        os.makedirs(os.path.dirname(label_path_dest), exist_ok=True)  # 确保目录存在

        with open(label_path_dest, 'w') as label_file:
            root = ET.parse(label_path_src).getroot()
            img_size = root.find('size')
            img_width = float(img_size.find('width').text)
            img_height = float(img_size.find('height').text)

            for obj in root.findall('object'):
                class_name = obj.find('name').text
                if class_name not in class_to_idx:
                    continue

                class_idx = class_to_idx[class_name]
                bbox = obj.find('bndbox')
                xmin = float(bbox.find('xmin').text)
                ymin = float(bbox.find('ymin').text)
                xmax = float(bbox.find('xmax').text)
                ymax = float(bbox.find('ymax').text)

                # 计算YOLO格式的坐标（中心点坐标、宽度和高度）
                x_center = (xmin + xmax) / (2 * img_width)
                y_center = (ymin + ymax) / (2 * img_height)
                width = (xmax - xmin) / img_width
                height = (ymax - ymin) / img_height

                # 将YOLO格式的标签写入文件
                label_file.write(f"{class_idx} {x_center:.6f} {y_center:.6f} {width:.6f} {height:.6f}\n")

# 对训练集和验证集执行标签转换
convert_voc_to_yolo_label(train_images, 'train')
convert_voc_to_yolo_label(val_images, 'val')

print("数据集转换完成，YOLO格式的数据集保存在", output_dir)
