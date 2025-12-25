from fastapi import FastAPI, UploadFile, File
import os
import uuid

from utils.image_utils import read_image_info
from utils.tiler import tile_image

app = FastAPI(title= "Autoslide ml service")

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@app.get("/")
def health_check():
    return {"status": "ml service is running"}

@app.post("/upload-image/")
async def upload_image(file: UploadFile = File(...)):

    #generate unique filename 
    ext = file.filename.split(".")[-1]
    filename = f"{uuid.uuid4()}.{ext}"
    file_path = os.path.join(UPLOAD_DIR, filename)

    #save file
    with open(file_path, "wb") as f:
        f.write(await file.read())

    #read image info
    image_info = read_image_info(file_path)

    return {
        "message": "Image uploaded successfully",
        "filename": filename, 
        "image_info": image_info
    }

@app.post("/tile-image/{filename}")
def tile_uploaded_image(filename: str):
    image_path = os.path.join(UPLOAD_DIR, filename)

    if not os.path.exists(image_path):
        return {"error": "File not found"}
    
    tiles_dir = os.path.join("uploads", "tiles", filename.split(".")[0] )

    result = tile_image(
        image_path = image_path,
        output_dir = tiles_dir,
        tile_size = 256,
        overlap = 0
    )

    return {
        "message": "Image tiled successfully",
        "tiling_info": {
            "image_width": result["image_width"],
            "image_height": result["image_height"],
            "tile_size": result["tile_size"],
            "num_tiles": result["num_tiles"]
        }
    }