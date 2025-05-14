import os
from PIL import Image
import cv2
import torch
from realesrgan import RealESRGANer

# 输入和输出文件夹路径
input_folder = r'C:\Users\userone\Desktop\wangqiu'
output_folder = r'C:\Users\userone\Desktop\wangqiu2'

# 如果输出文件夹不存在，则创建
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# 初始化Real-ESRGAN高清化模型
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
model_path = 'RealESRGAN_x4.pth'  # 需要提前下载Real-ESRGAN的预训练模型文件
upscaler = RealESRGANer(scale=4, model_path=model_path, device=device)

# 遍历文件夹中的所有图像
for img_name in os.listdir(input_folder):
    img_path = os.path.join(input_folder, img_name)

    # 打开图像并进行大小扩大10倍处理
    img = Image.open(img_path)
    img_large = img.resize((img.width * 10, img.height * 10), Image.ANTIALIAS)

    # 将放大的图像转换为OpenCV格式，以便进行高清化处理
    img_large_cv = cv2.cvtColor(np.array(img_large), cv2.COLOR_RGB2BGR)

    # 使用Real-ESRGAN对图像进行高清化处理
    output, _ = upscaler.enhance(img_large_cv)

    # 将高清化后的图像保存为JPEG格式
    output_img_name = os.path.splitext(img_name)[0] + '_hd.jpg'
    output_img_path = os.path.join(output_folder, output_img_name)
    cv2.imwrite(output_img_path, output)

    print(f"处理完毕：{output_img_name}")
