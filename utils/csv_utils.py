from typing import List, Dict
from models.pixel_bodypart import PixelBodypart

import csv

def amount_of_columns_in_cv(csv_file_path: str) -> int:
    '''
    Every deeplabcut csv file consists of a frame and then 3 columns per bodypart:
    x, y and likelihood. 
    
    This means the total amount of columns is 1 + bodyparts * 3.
    '''
    return len(read_csv_line(csv_file_path, 0))

def body_parts_in_csv(csv_file_path: str) -> Dict[str, int]:
    '''
    Every deeplabcut csv file has the bodyparts on the 2nd row.

    retuns a Dict[str, int] with key as bodypart and value as the column it starts on. 
    '''
    row = read_csv_line(csv_file_path, 1)
    body_parts = {}
    for i, s in enumerate(row):
        # 0 is always bodyparts and thus not needed.
        if i == 0: 
            continue

        if not (s in body_parts):
            body_parts[s] = i
    return body_parts

def read_csv_line(csv_file_path, line: int = 0):
    '''
    Read the csv file and return the wanted row in form of List[str]
    '''
    if line < 0:
        return []
    
    with open(csv_file_path) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        for row in csv_reader:
            if line_count == line:
                return row
            line_count += 1

def read_body_part(body_part: str, csv_file_path: str) -> List[PixelBodypart]:
    body_parts = body_parts_in_csv(csv_file_path)
    if body_part not in body_parts:
        return []
    
    frame_i = 0
    x_i = body_parts[body_part]
    y_i = x_i +1
    likelihood_i = x_i + 2

    results = []

    with open(csv_file_path) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        for row in csv_reader:
            # first 3 lines are metadata, not needed
            if line_count < 3:
                line_count += 1
                continue

            results.append(PixelBodypart(x=float(row[x_i]),frame=int(row[frame_i]), y=float(row[y_i]), body_part=body_part, likelihood=float(row[likelihood_i])))
    
    return results


    