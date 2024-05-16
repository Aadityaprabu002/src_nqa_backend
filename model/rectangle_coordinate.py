from typing import Tuple, List
class RectangleCoordinate:
    def __init__(self,x1:int,y1:int,x2:int,y2:int):
        self.x1 :int = x1
        self.y1 :int = y1
        self.x2 :int = x2
        self.y2 :int = y2
        self.xyxy = (self.x1,self.y1,self.x2,self.y2)
    
    def __init__(self, coordinate_list: Tuple[int]|List[int] ):
        self.x1 :int = coordinate_list[0]
        self.y1 :int = coordinate_list[1]
        self.x2 :int = coordinate_list[2]
        self.y2 :int = coordinate_list[3]
        self.xyxy = (self.x1,self.y1,self.x2,self.y2)
    
  