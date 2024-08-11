import matplotlib.pyplot as plt
import pandas as pd
import gc
import math
import utils.csv_utils as csv_utils
import utils.file_utils as file_utils

from typing import List
from models.pixel_bodypart import PixelBodypart
from analysis.utils.pixel_cm_convertor import PixelCmConvertor
from models.distance_interval import DistanceInterval

def trace_path(bodypart_pixels: List[PixelBodypart], output_file_path: str, frame_size: str = None, calculate_distance: bool = False, calculate_speed: bool = False):
    bodypart = 'Unknown'
    if(len(bodypart_pixels) > 0):
        bodypart = bodypart_pixels[0].body_part

    coords = [[point.x, point.y] for point in bodypart_pixels]
    df = pd.DataFrame(coords, columns=['x', 'y'])

    distance_calculated = False
    speed_calculated = False
    distance = 0
    speed = 0
    if frame_size is not None and isinstance(frame_size, str) and calculate_distance:
        distance = distance_travelled(coords, frame_size)
        distance_calculated = True
    
    if frame_size is not None and isinstance(frame_size, str) and calculate_speed:
        distance = distance_travelled(coords, frame_size)
        if len(bodypart_pixels) > 0 :
            speed = distance / (len(bodypart_pixels) / 10)
            speed_calculated = True
        
    plt.plot(df['x'], df['y'])
    plt.xlabel('X')
    plt.ylabel('Y')
    title = f'Path of mouse {bodypart}'
    if distance_calculated and not speed_calculated:
        title = title + f'\nDistance travelled is {round(distance, 2)} cm'
    
    if speed_calculated:
        title = title + f'\n Distance travelled is {round(distance, 2)} cm at {round(speed, 2)} cm / second'

    plt.title(title)

    plt.savefig(output_file_path, transparent=True)

    plt.cla()
    plt.clf()
    plt.close('all')
    gc.collect()

def distance_travelled(data: List[List[float]], frame_size: str, start: int = None, end: int = None):
    distance = 0
    if len(data) == 0:
        return distance
    
    r_start = 0
    r_end = len(data)

    if start is not None and end is not None and start <= end:
        r_start = start
        r_end = end

    max_x = max(value[0] for value in data)
    max_y = max(value[1] for value in data)
    pixel_convertor = PixelCmConvertor(frame_size, max_x, max_y)

    for i in range(r_start, r_end -1):
        current_point = pixel_convertor.convert_pixel_to_cm(data[i])
        next_point = pixel_convertor.convert_pixel_to_cm(data[i + 1])
        distance += math.dist(current_point, next_point)

    return distance

def create_path_analysis_table(csv_file: str, input_files: List[str], box_size: str, bodypart: str):
    csv = []
    header = []
    header.append('filename')
    header.append('distance in cm')
    header.append('speed in cm/second')
    csv.append(header)
    for file in input_files:
        file_name = file_utils.base_filename(file)
        data = csv_utils.read_body_part(bodypart, file)
        coords = [[point.x, point.y] for point in data]
        distance = distance_travelled(coords, box_size)
        speed = 0
        if len(data) > 0 :
            speed = distance / (len(data) / 10)
        row = []
        row.append(file_name)
        row.append(round(distance, 2))
        row.append(round(speed, 2))
        csv.append(row)
    csv_utils.write_to_csv(csv_file, csv)

def distance_interval_csv(bodypart_pixels: List[PixelBodypart], time_interval: int, box_size: str, csv_file: str):
    max_frame = len(bodypart_pixels)
    frame_interval = time_interval * 10
    interval_range = []
    current_range = 0
    for i in range(max_frame):
        if i  - current_range >= frame_interval:
            current_range = i
            interval_range.append(i)

    if max_frame - 1 not in interval_range:
        interval_range.append(max_frame -1)
    
    interval_start = 0

    coords = [[point.x, point.y] for point in bodypart_pixels]
    csv = []
    header = []
    header.append('Time in seconds')
    header.append('Distance in cm')
    header.append('Speed in cm / second')
    csv.append(header)
    for i in interval_range:
        row  = []
        row.append(round(i / 10))
        distance = distance_travelled( coords, box_size, interval_start, i)
        row.append(round(distance, 2))
        speed = distance / ((i - interval_start) / 10)
        row.append(round(speed, 2))
        interval_start = i
        csv.append(row)
    csv_utils.write_to_csv(csv_file, csv)


    