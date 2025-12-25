from fastapi import FastAPI, UploadFile, File
import os
import uuid

from utils.image_utils import read_image_info

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