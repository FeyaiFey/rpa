import os
import random
import shutil

# 设置路径
image_dir = 'images'
label_dir = 'labels'
train_image_dir = 'images/train'
test_image_dir = 'images/test'
train_label_dir = 'labels/train'
test_label_dir = 'labels/test'

# 创建目标文件夹
os.makedirs(train_image_dir, exist_ok=True)
os.makedirs(test_image_dir, exist_ok=True)
os.makedirs(train_label_dir, exist_ok=True)
os.makedirs(test_label_dir, exist_ok=True)

# 获取所有图片文件
image_files = [f for f in os.listdir(image_dir) if f.endswith('.jpg') or f.endswith('.png')]

# 打乱文件顺序
random.shuffle(image_files)

# 划分比例：80% 训练集，20% 测试集
split_ratio = 0.8
train_files = image_files[:int(len(image_files) * split_ratio)]
test_files = image_files[int(len(image_files) * split_ratio):]


# 将图片和标签文件分别复制到对应的文件夹
def move_files(files, image_dir, label_dir, target_image_dir, target_label_dir):
    for file in files:
        # 图片路径
        image_path = os.path.join(image_dir, file)
        # 标签路径
        label_path = os.path.join(label_dir, file.replace('.jpg', '.txt').replace('.png', '.txt'))

        # 移动图片和标签文件
        shutil.copy(image_path, target_image_dir)
        shutil.copy(label_path, target_label_dir)


# 移动文件
move_files(train_files, image_dir, label_dir, train_image_dir, train_label_dir)
move_files(test_files, image_dir, label_dir, test_image_dir, test_label_dir)

print(f"训练集包含 {len(train_files)} 张图片，测试集包含 {len(test_files)} 张图片。")
