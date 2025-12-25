from PIL import Image

def read_image_info(image_path: str):
    with Image.open(image_path) as img:
        return {
            "height": img.height,
            "width": img.width,
            "mode": img.mode,
            "format": img.format
        }
    
    