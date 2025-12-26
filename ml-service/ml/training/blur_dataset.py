import cv2
import random
import torch
from torch.utils.data import Dataset
from torchvision import transforms
from PIL import Image


class BlurTileDataset(Dataset):
    def __init__(self, tile_paths):
        self.tile_paths = tile_paths
        self.transform = transforms.Compose([
            transforms.Resize((256, 256)),
            transforms.ToTensor()
        ])

    def __len__(self):
        return len(self.tile_paths)

    def __getitem__(self, idx):
        img = cv2.imread(self.tile_paths[idx])
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

        # synthetic label
        label = random.choice([0, 1])  # 0=sharp, 1=blur
        if label == 1:
            img = cv2.GaussianBlur(img, (9, 9), 0)

        img = Image.fromarray(img)
        img = self.transform(img)

        return img, torch.tensor([label], dtype=torch.float32)
