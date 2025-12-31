import cv2
import numpy as np


def compute_stain_quality(image_path: str):
    """
    Returns stain quality score between 0 and 1
    Higher = better staining
    """
    img = cv2.imread(image_path)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    # Convert to LAB color space (good for color analysis)
    lab = cv2.cvtColor(img, cv2.COLOR_RGB2LAB)

    # Compute variance of A and B channels (color richness)
    a_channel = lab[:, :, 1]
    b_channel = lab[:, :, 2]

    color_variance = np.var(a_channel) + np.var(b_channel)

    # Normalize variance to 0–1 range
    stain_quality = min(color_variance / 5000.0, 1.0)

    return stain_quality
