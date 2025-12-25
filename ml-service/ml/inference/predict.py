import torch
from torchvision import transforms
from PIL import Image

from models.blur_model import BlurQualityModel

#load pre-trained model
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model = BlurQualityModel().to(device)
model.eval()

transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
])

def predict_tile(image_path: str) -> float:
    """
    Predict the blur quality score of a tile image.
    Returns a float score between 0 and 1.
    """
    img = Image.open(image_path).convert("RGB")
    x = transform(img).unsqueeze(0).to(device)

    with torch.no_grad():
        score = model(x).item()
     
    return score