#voc 转coco，分三个文件夹，xml2txt
import os
import shutil
import xml.etree.ElementTree as ET

# 文件路径
voc_dir = r'C:\Users\userone\Desktop\6900DSAlast'
jpeg_images_dir = os.path.join(voc_dir, 'JPEGImages')
annotations_dir = os.path.join(voc_dir, 'Annotations')

# 输出路径
output_images_dir = os.path.join(voc_dir, 'Labels', 'images')
output_xml_dir = os.path.join(voc_dir, 'Labels', 'xml')
output_labels_dir = os.path.join(voc_dir, 'Labels', 'labels')

# 文件名列表
splits = ['train', 'val', 'test']

# 创建输出文件夹
for split in splits:
    os.makedirs(os.path.join(output_images_dir, split), exist_ok=True)
    os.makedirs(os.path.join(output_xml_dir, split), exist_ok=True)
    os.makedirs(os.path.join(output_labels_dir, split), exist_ok=True)

# 复制图像文件和XML文件
def copy_files(file_list, src_dir, dest_dir, extension):
    for file_name in file_list:
        src_path = os.path.join(src_dir, file_name + extension)
        dest_path = os.path.join(dest_dir, file_name + extension)
        shutil.copy(src_path, dest_path)

# 读取文件名列表
def read_file_list(split):
    with open(os.path.join(voc_dir, f'{split}.txt')) as f:
        return [line.strip() for line in f]

# 复制图像和XML文件
for split in splits:
    file_list = read_file_list(split)
    copy_files(file_list, jpeg_images_dir, os.path.join(output_images_dir, split), '.jpg')
    copy_files(file_list, annotations_dir, os.path.join(output_xml_dir, split), '.xml')

class_to_idx = {
    'catheter': 0,
    'guidewire': 1,
    'spring': 2,
    # 如果你的数据集有更多类别，请继续添加映射
}

# 转换XML标签为YOLO格式并保存为txt文件
def convert_voc_to_yolo_label(file_list, subset):
    for file_name in file_list:
        label_path_src = os.path.join(output_xml_dir, subset, file_name + '.xml')
        label_path_dest = os.path.join(output_labels_dir, subset, file_name + '.txt')

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

# 对训练集、验证集和测试集执行标签转换
for split in splits:
    file_list = read_file_list(split)
    convert_voc_to_yolo_label(file_list, split)

print("数据集转换完成，YOLO格式的数据集保存在", voc_dir)
