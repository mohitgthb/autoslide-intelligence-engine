import os
from PIL import Image

def tile_image(
    image_path: str, 
    output_dir: str,
    tile_size: int = 256,
    overlap: int = 0
):
    """
    Split an image into tiles and save them.

    Returns metadata about tiling.
    """
    os.makedirs(output_dir, exist_ok=True)
    img = Image.open(image_path).convert("RGB")
    width, height = img.size

    tiles = []
    tile_id = 0

    step = tile_size - overlap

    for y in range(0, height - tile_size + 1, step):
        for x in range(0, width - tile_size +1, step):
            tile = img.crop((x, y, x+tile_size, y+tile_size))

            tile_filename = f"tile_{tile_id}.png"
            tile_path = os.path.join(output_dir, tile_filename)
            tile.save(tile_path)

            tiles.append({
                "tile_id": tile_id,
                "x": x,
                "y": y,
                "file_path": tile_path
            })

            tile_id += 1

        img.close()

        return {
            "image_width": width,
            "image_height": height,
            "tile_size": tile_size,
            "overlap": overlap,
            "num_tiles": len(tiles),
            "tiles": tiles
        }
 