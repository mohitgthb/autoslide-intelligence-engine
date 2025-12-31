import cv2
import numpy as np

def compute_tissue_coverage(image_path: str):
    """return tissue coverage ratio"""

    # Read the image
    image = cv2.imread(image_path)

    # Convert to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    #Otsu thresholding to separate tissue from background
    _,mask = cv2.threshold(
        gray, 0, 255,
        cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU
    )

    #Morphological cleanup
    kernel = np.ones((5, 5), np.uint8)
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)

    tissue_pixels = cv2.countNonZero(mask)
    total_pixels = mask.shape[0] * mask.shape[1]

    return tissue_pixels / total_pixels