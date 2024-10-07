import gc
from typing import List

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.colors import PowerNorm

from models.pixel_bodypart import PixelBodypart


def plot_density_map_continous(
    bodypart_pixels: List[PixelBodypart], output_file_path: str
):
    """
    Generate and save a density heatmap for the coordinates of a specific body part.

    Args:
        bodypart_pixels (List[PixelBodypart]): A list of PixelBodypart objects.
        output_file_path (str): Path where the output heatmap image will be saved.
    """
    bodypart = bodypart_pixels[0].body_part if bodypart_pixels else "Unknown"

    coords = [[point.x, point.y] for point in bodypart_pixels]
    df = pd.DataFrame(coords, columns=["x", "y"])

    H, xedges, yedges = np.histogram2d(df["x"], df["y"], bins=(100, 100))

    X, Y = np.meshgrid(xedges[:-1], yedges[:-1])

    plt.imshow(
        H.T,
        extent=[X.min(), X.max(), Y.min(), Y.max()],
        origin="lower",
        interpolation="bicubic",
        cmap=plt.cm.jet,
        norm=PowerNorm(0.3),
    )

    plt.xlabel("X Coordinate")
    plt.ylabel("Y Coordinate")
    plt.colorbar(label="Density")
    plt.title(f"Heatmap of Coordinates (Interpolared bicubic) for {bodypart}")

    plt.savefig(output_file_path, transparent=True)

    plt.cla()
    plt.clf()
    plt.close("all")
    gc.collect()
