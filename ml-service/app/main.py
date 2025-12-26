from fastapi import FastAPI, UploadFile, File
import os
import uuid

from utils.image_utils import read_image_info
from utils.tiler import tile_image
from ml.inference.aggregate import predict_slide_quality
from utils.heatmap import generate_tile_heatmap
from utils.tile_manager import manage_tiles

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

@app.post("/analyze-slide/{filename}")
def analyze_slide(filename: str):
    tiles_dir = os.path.join("uploads", "tiles", filename.split(".")[0])

    if not os.path.exists(tiles_dir):
        return {"error": "Tiles directory not found"}
    
    result = predict_slide_quality(tiles_dir)

    return {
        "message": "Slide analysis completed",
        "analysis_result": result
    }

@app.post("/heatmap/{filename}")
def generate_heatmap(filename: str):
    image_path = os.path.join(UPLOAD_DIR, filename)
    tiles_dir = os.path.join("uploads", "tiles", filename.split(".")[0])

    analysis = predict_slide_quality(tiles_dir)

    heatmap_img = generate_tile_heatmap(
        original_image_path = image_path,   
        tiles_info = analysis["tiles"]
    )

    heatmap_path = os.path.join(UPLOAD_DIR, f"heatmap_{filename}")
    heatmap_img.save(heatmap_path)

    return {
        "message": "Heatmap generated successfully",
        "heatmap_path": heatmap_path
    }

@app.post("/manage-tiles/{filename}")
def manage_image_tiles(filename: str, max_tiles: int = 1000, sample_rate: float = 0.3):
    tiles_dir = os.path.join("uploads", "tiles", filename.split(".")[0])

    if not os.path.exists(tiles_dir):
        return {"error": "Tiles directory not found"}
    
    manage_tiles(
        tile_dir = tiles_dir,
        max_tiles = max_tiles,
        sample_rate = sample_rate
    )

    return {
        "message": "Tile management completed"
    }

