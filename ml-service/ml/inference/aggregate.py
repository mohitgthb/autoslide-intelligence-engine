import os
from ml.inference.predict import predict_tile

def predict_slide_quality(tiles_dir: str):
    scores = []

    for file in os.listdir(tiles_dir):
        if file.endswith(".png") or file.endswith(".jpg") or file.endswith(".jpeg"):
            tile_path = os.path.join(tiles_dir, file)
            score = predict_tile(tile_path)
            scores.append({
                "tile": file,
                "score": score
            })

    if not scores:
        return None
    
    tile_scores = [s["score"] for s in scores]
    
    return {
        "num_tiles": len(tile_scores),
        "average_score": sum(tile_scores) / len(tile_scores),
        "min_score": min(tile_scores),
        "max_score": max(tile_scores),
        "tiles": scores
    }