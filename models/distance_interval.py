from dataclasses import dataclass

@dataclass(frozen = True)
class DistanceInterval:
    '''Class that represents a deeplabcut pixel object for a bodypart'''
    time: int
    distance: float 
    speed: float