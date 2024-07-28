from dataclasses import dataclass

@dataclass(frozen = True)
class PixelBodypart:
    '''Class that represents a deeplabcut pixel object for a bodypart'''
    x: float
    y: float
    body_part: str 
    frame: int
    likelihood:float