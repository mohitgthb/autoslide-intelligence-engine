import glob
import torch
import torch.nn as nn
from torch.utils.data import DataLoader
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))


from models.blur_model import BlurQualityModel
from ml.training.blur_dataset import BlurTileDataset

DEVICE = "cuda" if torch.cuda.is_available() else "cpu"  # change to "cuda" if available
BATCH_SIZE = 16
EPOCHS = 5
LR = 1e-4

# Use already-stored tiles (NO duplication)
tile_paths = glob.glob("uploads/tiles/*/*.png")

# (Optional) limit for bootstrap training
tile_paths = tile_paths[:1000]

dataset = BlurTileDataset(tile_paths)
loader = DataLoader(dataset, batch_size=BATCH_SIZE, shuffle=True)

model = BlurQualityModel().to(DEVICE)
criterion = nn.BCELoss()
optimizer = torch.optim.Adam(model.parameters(), lr=LR)

for epoch in range(EPOCHS):
    running_loss = 0.0
    for x, y in loader:
        x, y = x.to(DEVICE), y.to(DEVICE)

        pred = model(x)
        loss = criterion(pred, y)

        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

        running_loss += loss.item()

    print(f"Epoch {epoch+1}/{EPOCHS} | Loss: {running_loss/len(loader):.4f}")

# Save trained weights
torch.save(model.state_dict(), "models/blur_model.pt")
print("✅ Blur model trained and saved")
