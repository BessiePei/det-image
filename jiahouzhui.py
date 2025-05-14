import os

# 指定要处理的文件夹路径
folder_path = r'C:\Users\userone\Desktop\搜狗图片搜索 - 网球_files'

# 遍历文件夹中的所有文件
for filename in os.listdir(folder_path):
    # 拼接文件的完整路径
    file_path = os.path.join(folder_path, filename)

    # 检查是否是文件而不是文件夹
    if os.path.isfile(file_path):
        # 获取文件名和扩展名
        name, ext = os.path.splitext(filename)

        # 检查扩展名是否不是.jpg，如果不是则添加.jpg后缀
        if ext.lower() != '.jpg':
            new_filename = name + '.jpg'
            new_file_path = os.path.join(folder_path, new_filename)

            # 重命名文件
            os.rename(file_path, new_file_path)
            print(f'已更改文件：{filename} 为 {new_filename}')

print('所有文件处理完毕。')
