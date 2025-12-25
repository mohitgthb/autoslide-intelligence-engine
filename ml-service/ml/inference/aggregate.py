import os
from ml.inference.predict import predict_tile

def predict_slide_quality(tiles_dir: str):
    scores = []

    for file in os.listdir(tiles_dir):
        if file.endswith(".png") or file.endswith(".jpg") or file.endswith(".jpeg"):
            tile_path = os.path.join(tiles_dir, file)
            score = predict_tile(tile_path)
            scores.append(score)

    if not scores:
        return None
    
    return {
        "num_tiles": len(scores),
        "average_score": sum(scores) / len(scores),
        "min_score": min(scores),
        "max_score": max(scores)
    }