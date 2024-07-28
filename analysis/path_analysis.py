import matplotlib.pyplot as plt
import pandas as pd

from typing import List
from models.pixel_bodypart import PixelBodypart

def trace_path(bodypart_pixels: List[PixelBodypart], output_file_path: str):
    bodypart = 'Unknown'
    if(len(bodypart_pixels) > 0):
        bodypart = bodypart_pixels[0].body_part

    coords = [[point.x, point.y] for point in bodypart_pixels]
    df = pd.DataFrame(coords, columns=['x', 'y'])

    plt.plot(df['x'], df['y'])
    plt.xlabel('X')
    plt.ylabel('Y') 
    plt.title(f'Path of mouse {bodypart}')

    plt.savefig(output_file_path, transparent=True)