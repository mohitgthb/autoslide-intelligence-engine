import os
import random

def manage_tiles(tile_dir, max_tiles=1000, sample_rate=0.3):
    """
    Keeps only a subset of tiles:
    - randomly samples tiles
    - enforces a maximum limit
    """

    if not os.path.exists(tile_dir):
        return

    tiles = [f for f in os.listdir(tile_dir) if f.endswith(".png")]

    # random sampling
    sampled = [t for t in tiles if random.random() < sample_rate]

    # enforce max limit
    if len(sampled) > max_tiles:
        sampled = random.sample(sampled, max_tiles)

    # delete unselected tiles
    for t in tiles:
        if t not in sampled:
            os.remove(os.path.join(tile_dir, t))
