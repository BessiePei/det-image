# from PIL import Image
# import os
# from tqdm import tqdm
import os
from PIL import Image
import numpy as np
import cv2
from tqdm import tqdm


def resize_image(image_path, scale_factor=3, interpolation=Image.LINEAR):
    try:
        image = Image.open(image_path)  # 打开图像文件
        original_size = image.size  # 获取图像的原始尺寸 (宽度, 高度)
        new_size = (original_size[0] * scale_factor, original_size[1] * scale_factor)  # 计算新尺寸
        resized_image = image.resize(new_size, interpolation)  # 调整图像大小
        return resized_image  # 返回调整大小后的图像
    except Exception as e:
        print(f"Error resizing image {image_path}: {e}")  # 打印错误信息
        return None


def enhance_image(image):
    # 将PIL图像转换为NumPy数组
    image_np = np.array(image)

    # 使用OpenCV进行图像锐化处理
    kernel = np.array([[0, -1, 0],
                       [-1, 5, -1],
                       [0, -1, 0]])
    sharpened_image = cv2.filter2D(image_np, -1, kernel)  # 锐化图像

    # 将NumPy数组转换回PIL图像
    return Image.fromarray(sharpened_image)


ori_image_dir = r'C:\Users\userone\Desktop\sougou'
save_image_dir = r"C:\Users\userone\Desktop\sougou_3"

if not os.path.exists(save_image_dir):
    os.makedirs(save_image_dir)

for ori_image in tqdm(os.listdir(ori_image_dir)):
    image_path = os.path.join(ori_image_dir, ori_image)
    output_image = resize_image(image_path, interpolation=Image.LINEAR)
    if output_image:
        enhanced_image = enhance_image(output_image)  # 增强图像清晰度
        output_path = os.path.join(save_image_dir, ori_image)
        try:
            enhanced_image.save(output_path)
        except Exception as e:
            print(f"Error saving image {output_path}: {e}")

# import numpy as np
#
#
# def resize_image(image_path, scale_factor=3, interpolation=Image.LINEAR):
#     try:
#         image = Image.open(image_path)  # 打开图像文件
#         original_size = image.size  # 获取图像的原始尺寸 (宽度, 高度)
#         new_size = (original_size[0] * scale_factor, original_size[1] * scale_factor)  # 计算新尺寸
#         resized_image = image.resize(new_size, interpolation)  # 调整图像大小
#         return resized_image  # 返回调整大小后的图像
#     except Exception as e:
#         print(f"Error resizing image {image_path}: {e}")  # 打印错误信息
#         return None
#
#
# ori_image_dir = r'C:\Users\userone\Desktop\sougou'
# save_image_dir = r"C:\Users\userone\Desktop\sougou_512x512"
#
# if not os.path.exists(save_image_dir):
#     os.makedirs(save_image_dir)
#
# for ori_image in tqdm(os.listdir(ori_image_dir)):
#     image_path = os.path.join(ori_image_dir, ori_image)
#     output_image = resize_image(image_path, interpolation=Image.LINEAR)
#     if output_image:
#         output_path = os.path.join(save_image_dir, ori_image)
#         try:
#             output_image.save(output_path)
#         except Exception as e:
#             print(f"Error saving image {output_path}: {e}")
