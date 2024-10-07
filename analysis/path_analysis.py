import gc
import math
from typing import List

import matplotlib.pyplot as plt
import pandas as pd

import utils.csv_utils as csv_utils
import utils.file_utils as file_utils
from analysis.utils.pixel_cm_convertor import PixelCmConvertor
from models.pixel_bodypart import PixelBodypart
from utils.constants import FRAME_RATE


def trace_path(
    bodypart_pixels: List[PixelBodypart],
    output_file_path: str,
    frame_size: str = None,
    calculate_distance: bool = False,
    calculate_speed: bool = False,
):
    if not bodypart_pixels:
        return

    bodypart = bodypart_pixels[0].body_part if len(bodypart_pixels) > 0 else "Unknown"

    coords = [[point.x, point.y] for point in bodypart_pixels]
    df = pd.DataFrame(coords, columns=["x", "y"])

    distance = speed = 0
    distance_calculated = speed_calculated = False

    if frame_size is not None and isinstance(frame_size, str) and calculate_distance:
        distance = distance_travelled(coords, frame_size)
        distance_calculated = True

    if frame_size is not None and isinstance(frame_size, str) and calculate_speed:
        distance = distance_travelled(coords, frame_size)
        if len(bodypart_pixels) > 0:
            speed = distance / (len(bodypart_pixels) / FRAME_RATE)
            speed_calculated = True

    plt.plot(df["x"], df["y"])
    plt.xlabel("X")
    plt.ylabel("Y")
    title = f"Path of mouse {bodypart}"
    if distance_calculated and not speed_calculated:
        title = title + f"\nDistance travelled is {round(distance, 2)} cm"

    if speed_calculated:
        title = (
            title
            + f"\n Distance travelled is {round(distance, 2)} cm"
            + f" at {round(speed, 2)} cm / second"
        )

    plt.title(title)

    plt.savefig(output_file_path, transparent=True)

    plt.cla()
    plt.clf()
    plt.close("all")
    gc.collect()


def distance_travelled(
    data: List[List[float]], frame_size: str, start: int = None, end: int = None
):
    """
    Calculates the total distance traveled based on pixel data.

    Args:
        data (List[List[float]]): A list of [x, y] coordinates.
        frame_size (str): The frame size used for converting pixels to centimeters.
        start (int, optional): Starting index for calculation.
        end (int, optional): Ending index for calculation.

    Returns:
        float: Total distance traveled in centimeters.
    """
    if len(data) == 0:
        return 0

    r_start = start if start is not None else 0
    r_end = end if end is not None else len(data)

    max_x = max(value[0] for value in data)
    max_y = max(value[1] for value in data)
    pixel_convertor = PixelCmConvertor(frame_size, max_x, max_y)

    distance = 0
    for i in range(r_start, r_end - 1):
        current_point = pixel_convertor.convert_pixel_to_cm(data[i])
        next_point = pixel_convertor.convert_pixel_to_cm(data[i + 1])
        distance += math.dist(current_point, next_point)

    return distance


def create_path_analysis_table(
    csv_file: str, input_files: List[str], box_size: str, bodypart: str
):
    """
    Creates a CSV table summarizing the distance and speed for each input file.

    Args:
        csv_file (str): Path to save the resulting CSV file.
        input_files (List[str]): List of file paths to process.
        box_size (str): Size of the frame to calculate distance in centimeters.
        bodypart (str): The body part whose movement is being analyzed.

    Returns:
        None
    """
    csv = [["filename", "distance in cm", "speed in cm/second"]]
    for file in input_files:
        file_name = file_utils.base_filename(file)
        data = csv_utils.read_body_part(bodypart, file)
        coords = [[point.x, point.y] for point in data]
        distance = distance_travelled(coords, box_size)
        speed = distance / (len(data) / 10) if len(data) > 0 else 0
        csv.append([file_name, round(distance, 2), round(speed, 2)])
    csv_utils.write_to_csv(csv_file, csv)


def distance_interval_csv(
    bodypart_pixels: List[PixelBodypart],
    time_interval: int,
    box_size: str,
    csv_file: str,
):
    """
    Creates a CSV file recording distance and speed at regular time intervals.

    Args:
        bodypart_pixels (List[PixelBodypart]): List of pixel coordinates for
        the body part.
        time_interval (int): The interval (in seconds) for recording distances.
        box_size (str): The size of the frame for converting pixel data to centimeters.
        csv_file (str): Path to save the resulting CSV file.

    Returns:
        None
    """
    max_frame = len(bodypart_pixels)
    frame_interval = time_interval * FRAME_RATE
    interval_range = []
    current_range = 0
    for i in range(max_frame):
        if i - current_range >= frame_interval:
            current_range = i
            interval_range.append(i)

    if max_frame - 1 not in interval_range:
        interval_range.append(max_frame - 1)

    interval_start = 0

    coords = [[point.x, point.y] for point in bodypart_pixels]
    csv = [["Time in seconds", "Distance in cm", "Speed in cm/second"]]
    for i in interval_range:
        row = []
        time_in_seconds = round(i / FRAME_RATE)
        distance, speed = calculate_speed_and_distance(
            coords, interval_start, i, box_size
        )
        csv.append([time_in_seconds, round(distance, 2), round(speed, 2)])
        interval_start = i
        csv.append(row)
    csv_utils.write_to_csv(csv_file, csv)


def calculate_speed_and_distance(
    coords: List[List[float]], start: int, end: int, box_size: str
):
    """
    Helper function to calculate both distance and speed.

    Args:
        coords (List[List[float]]): List of [x, y] coordinates.
        start (int): Starting index for calculation.
        end (int): Ending index for calculation.
        box_size (str): The size of the frame for converting pixel data to centimeters.

    Returns:
        Tuple[float, float]: Distance in cm, speed in cm/second.
    """
    distance = distance_travelled(coords, box_size, start, end)
    speed = distance / ((end - start) / FRAME_RATE) if (end - start) > 0 else 0
    return distance, speed
