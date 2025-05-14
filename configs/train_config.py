from torch import optim

from datasets.coco import CocoDetection
from transforms import presets
from optimizer import param_dict

# Commonly changed training configurations
num_epochs = 40  # train epochs
batch_size = 2  # total_batch_size = #GPU x batch_size
num_workers = 1  # workers for pytorch DataLoader
pin_memory = True  # whether pin_memory for pytorch DataLoader
print_freq = 50  # frequency to print logs
starting_epoch = 0
max_norm = 0.1  # clip gradient norm

output_dir = None  # path to save checkpoints, default for None: checkpoints/{model_name}
find_unused_parameters = False  # useful for debugging distributed training

# define dataset for train
# coco_path = r"C:\Users\userone\Desktop\rtdetr_pytorch\configs\dataset\coco6700xin"  # /PATH/TO/YOUR/COCODIR
coco_path = r'D:\SFDSA\Salience-DETR-main\datasets\coco6900xin'
train_transform = presets.detr  # see transforms/presets to choose a transform
train_dataset = CocoDetection(
    img_folder=f"{coco_path}/train",
    ann_file=f"{coco_path}\instances_train2017.json",
    transforms=train_transform,
    train=True,
)
test_dataset = CocoDetection(
    img_folder=f"{coco_path}/val",
    ann_file=f"{coco_path}\instances_val2017.json",
    transforms=None,  # the eval_transform is integrated in the model
)

# model config to train
model_path = "configs\salience_detr\salience_detr_resnet50_800_1333.py"

# specify a checkpoint folder to resume, or a pretrained ".pth" to finetune, for example:
# checkpoints/salience_detr_resnet50_800_1333/train/2024-03-22-09_38_50
# checkpoints/salience_detr_resnet50_800_1333/train/2024-03-22-09_38_50/best_ap.pth
# resume_from_checkpoint = None
# resume_from_checkpoint = 'checkpoints/salience_detr_resnet50_800_1333-px/train/2024-12-09-16_22_25-dlB/best_ap.pth'
resume_from_checkpoint = 'checkpoints/train/2024-10-22-09_35_02/best_ap.pth'

learning_rate = 1e-4  # initial learning rate
optimizer = optim.AdamW(lr=learning_rate, weight_decay=1e-4, betas=(0.9, 0.999))
lr_scheduler = optim.lr_scheduler.MultiStepLR(milestones=[10], gamma=0.1)

# This define parameter groups with different learning rate
param_dicts = param_dict.finetune_backbone_and_linear_projection(lr=learning_rate)
