import os
import cv2
import numpy as np
from PIL import Image

def generate_tile_heatmap(original_image_path: str, tiles_info: list, tile_size: int = 256):
    img = Image.open(original_image_path).convert("RGB")
    heatmap = np.zeros((img.height, img.width), dtype=np.float32)

    tiles_per_row = img.width // tile_size

    for tile in tiles_info:
        tile_id = int(tile["tile"].split("_")[1].split(".")[0])
        score = tile["score"]

        row = tile_id // tiles_per_row
        col = tile_id % tiles_per_row

        y1 = row * tile_size
        x1 = col * tile_size

        heatmap[y1:y1+tile_size, x1:x1+tile_size] = score

    heatmap = cv2.normalize(heatmap, None, 0, 255, cv2.NORM_MINMAX)
    heatmap = heatmap.astype(np.uint8)
    heatmap = cv2.applyColorMap(heatmap, cv2.COLORMAP_JET)

    overlay = cv2.addWeighted(np.array(img), 0.6, heatmap, 0.4, 0)
    return Image.fromarray(overlay)
