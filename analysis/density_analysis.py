import matplotlib.pyplot as plt
from matplotlib.colors import PowerNorm
import pandas as pd
import numpy as np
import gc

from typing import List
from models.pixel_bodypart import PixelBodypart

def plot_density_map(bodypart_pixels: List[PixelBodypart]):
    bodypart = 'Unknown'
    if(len(bodypart_pixels) > 0):
        bodypart = bodypart_pixels[0].body_part

    coords = [[point.x, point.y] for point in bodypart_pixels]
    df = pd.DataFrame(coords, columns=['x', 'y'])

    plt.hist2d(x=df['x'], y=df['y'], bins=(100,100), cmap=plt.cm.jet, norm=PowerNorm(0.3)) 

    plt.xlabel('X Coordinate')
    plt.ylabel('Y Coordinate')

    plt.colorbar(label='Density')
    plt.title(f'Heatmap of Coordinates (Histogram) for {bodypart}')
    
    plt.show()

def plot_density_map_continous(bodypart_pixels: List[PixelBodypart], output_file_path: str):
    bodypart = 'Unknown'
    if(len(bodypart_pixels) > 0):
        bodypart = bodypart_pixels[0].body_part

    coords = [[point.x, point.y] for point in bodypart_pixels]
    df = pd.DataFrame(coords, columns=['x', 'y'])

    H, xedges, yedges = np.histogram2d(df['x'], df['y'], bins=(100, 100))

    X, Y = np.meshgrid(xedges[:-1], yedges[:-1])

    # Plottingx
    #plt.pcolormesh(X, Y, H.T, cmap=plt.cm.jet, norm=PowerNorm(0.3), shading="gouraud")
    plt.imshow(H.T, extent=[X.min(), X.max(), Y.min(), Y.max()], origin='lower', interpolation='bicubic', cmap=plt.cm.jet, norm=PowerNorm(0.3))


    plt.xlabel('X Coordinate')
    plt.ylabel('Y Coordinate')
    plt.colorbar(label='Density')
    plt.title(f'Heatmap of Coordinates (Interpolared bicubic) for {bodypart}')

    plt.savefig(output_file_path, transparent=True)

    plt.cla()
    plt.clf()
    plt.close('all')
    gc.collect()


