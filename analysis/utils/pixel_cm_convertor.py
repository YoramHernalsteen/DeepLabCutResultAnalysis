from typing import List

class PixelCmConvertor:
    ratio_width = 1
    ratio_length = 1

    def __init__(self, ratio_s: str, max_x: float, max_y: float):
        ratio_s = ratio_s.upper()
    
        length_s, width_s = ratio_s.split("X", 1)
        length_s = length_s.replace(',', '.')
        width_s = width_s.replace(',', '.')

        width = float(width_s) / max_x
        length = float(length_s) / max_y

        self.ratio_width = width
        self.ratio_length = length

    def convert_pixel_to_cm(self, pixel: List[float]):
        result = [0, 0]
        result[0] = pixel[0] * self.ratio_width
        result[1] = pixel[1] * self.ratio_length
        return result
