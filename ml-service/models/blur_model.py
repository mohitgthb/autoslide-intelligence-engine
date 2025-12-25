import torch 
import torch.nn as nn
from torchvision import models

class BlurQualityModel(nn.Module):
    def __init__(self):
        super().__init__()

        #use a pre-trained ResNet model as the backbone
        self.backbone = models.resnet18(pretrained=True)

        #replace classifier
        self.backbone.fc = nn.Sequential(
            nn.Linear(self.backbone.fc.in_features, 1),
            nn.Sigmoid()  #output beetween 0 and 1
        )

    def forward(self, x):
        return self.backbone(x)
    
    #These gives the quality score between 0 and 1 based on blur level
    