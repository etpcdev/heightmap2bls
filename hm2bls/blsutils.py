from dataclasses import dataclass
from enum import Flag, auto
import numpy as np
import math

#.bls file header contents
BLS_HEADER_WARNING = "This is a Blockland save file.  You probably shouldn't modify it cause you'll screw it up."
BLS_HEADER_DESCRIPTION = """1
Map Generated with hm2bls"""
BLS_HEADER_LINECOUNT = "Linecount "


@dataclass
class BLS_Color:
    #defines an rgba color on a scale of 0.0 -> 1.0
    r: float
    g: float
    b: float
    a: float
    
    def __hash__(self):
        return hash((self.r, self.g, self.b, self.a))
    
    def __eq__(self, other):
        if isinstance(other, BLS_Color):
            return (self.r, self.g, self.b, self.a) == (other.r, other.g, other.b, other.a)
        return False
    
class BLS_ColorSet:
    #for working with blockland colorsets
    def __init__(self,*, path: str = ""):
        assert path != "", "Empty path to colorset"
        
        self.mapped_colors = {}
        self.colorset = []
        self.__count = 0
        self.__colorset_str = ""
        
        with open(path,"r") as file:
            __column = []
            for line in file:
                if line != '\n':
                    if "DIV" in line.split(":"):
                        continue
                    else:
                        line = line.split()
                        __r = float(line[0])
                        __g = float(line[1])
                        __b = float(line[2])
                        __a = float(line[3])
                        
                        if __r > 1 or __g > 1 or __b > 1 or __a > 1:
                            __r = __r/255
                            __g = __g/255
                            __b = __b/255
                            __a = __a/255
                        
                        __color = BLS_Color(__r, __g, __b, __a)
                        __column.append(__color)
                        self.mapped_colors[hash(__color)] = self.__count
                        self.__count += 1
                        
                else:
                    self.colorset.append(__column)
                    __column = []
        
    def get_colorset(self):
        #returns the string needed by the .bls file that defines the colorset used on a save
        
        #has a trailing newline
        for column in self.colorset:
            for color in column:
                if isinstance(color, BLS_Color):
                    self.__colorset_str += f"{color.r:.6f} {color.g:.6f} {color.b:.6f} {color.a:.6f}\n"
            
        remainder = 64 - self.__count
        
        while remainder > 0:
            self.__colorset_str += "1.000000 0.000000 1.000000 0.000000\n"
            remainder -= 1
                
        return self.__colorset_str
    
    def map_colors(self, color_map: np.ndarray) -> np.ndarray:
        #attempts to map the colors provided by color_map to the colors available in the colorset
        #calculates the shortest euclidian distance in 4d color space
        
        cm = color_map.astype(np.float32)
        cm = (cm / 255)
        
        csm = np.zeros((cm.shape[0], cm.shape[1]), dtype=np.uint8)
        
        seen = set()
        new_color_hash_index = {}
        
        for i in range(0, len(cm)):
            for j in range(0,len(cm[0])):
                color_hash = hash((cm[i][j][0],cm[i][j][1],cm[i][j][2],cm[i][j][3]))
                if color_hash in seen:
                    csm[i][j] = self.mapped_colors[new_color_hash_index[color_hash]]
                else:
                    min_distance = float('inf')
                    closest_color = None
                    for col in self.colorset:
                        for color in col:
                            if isinstance(color, BLS_Color):
                                distance = math.sqrt(
                                    (float(cm[i][j][0]) - color.r)**2 +
                                    (float(cm[i][j][1]) - color.g)**2 +
                                    (float(cm[i][j][2]) - color.b)**2 +
                                    (float(cm[i][j][3]) - color.a)**2
                                )
                                if distance < min_distance:
                                    min_distance = distance
                                    closest_color = color
                    seen.add(color_hash)
                    new_color_hash_index[color_hash] = hash(closest_color)              
                    csm[i][j] = self.mapped_colors[hash(closest_color)]

        return csm


class BLS_BDFlags(Flag):
    #Flags for defining what additional data a brick contains
    OWNER = auto()
    EVENT = auto()
    EMITTER = auto()
    LIGHT = auto()
    ITEM = auto()
    
    
@dataclass
class BLS_OwnerData():
    #owner's BL_ID (blockland ID)
    ow_bl_id: int = 999999


@dataclass
class BLS_EventData():
    #data used to define a single event
    ev_delay: int = 0
    ev_enabled: int = 1
    ev_input: str = ""
    ev_unknown: int = 0
    ev_target: str = ""
    ev_output: str = ""
    ev_output_field: int = 0
    
    
@dataclass
class BLS_EmitterData():
    em_ui_name: str
    em_direction: str
    
    
@dataclass
class BLS_LightData():
    li_ui_name: str
    li_unknown: int = 1
    
    
@dataclass
class BLS_ItemData():
    it_ui_name: str
    it_direction: int = 2
    it_position: int = 2
    it_respawn_time: int = 4000


class BLS_BrickData:
    #constructs the additional data portion of a brick in a .bls file (directly under the line that defines its' position. denoted by a "+-TYPE")
    def __init__(self, flags: BLS_BDFlags, *, 
                 owner_data: BLS_OwnerData | None = None,
                 event_data: BLS_EventData | list[BLS_EventData] | None = None,
                 emitter_data: BLS_EmitterData | None = None,
                 light_data: BLS_LightData | None = None,
                 item_data:  BLS_ItemData  | None = None) -> None:
        self.data = ""
        
        if BLS_BDFlags.OWNER in flags:
            self.data += "+-OWNER " + str(owner_data.ow_bl_id) + "\n"
        
        if BLS_BDFlags.EVENT in flags:
            if len(event_data) == 1:
                self.data += "+-EVENT " + str(event_data.ev_delay) + " " + str(event_data.ev_enabled) + " " + event_data.ev_input + " " + str(event_data.ev_unknown) + " " + event_data.ev_target + " " + event_data.ev_output + " " + str(event_data.ev_output_field) + "\n"
            else:
                for event in event_data:
                    if isinstance(event, BLS_EventData):
                        self.data += "+-EVENT " + str(event.ev_delay) + " " + str(event.ev_enabled) + " " + event.ev_input + " " + str(event.ev_unknown) + " " + event.ev_target + " " + event.ev_output + " " + str(event.ev_output_field) + "\n"
        
        if BLS_BDFlags.EMITTER in flags:
            self.data += "+-EMITTER " + emitter_data.em_ui_name + " " + str(emitter_data.em_direction) + "\n"
        
        if BLS_BDFlags.LIGHT in flags:
            self.data += "+-LIGHT " + light_data.li_ui_name + " " + str(light_data.li_unknown) + "\n"
        
        if BLS_BDFlags.ITEM in flags:
            self.data += "+-ITEM " + item_data.it_ui_name + " " + str(item_data.it_direction) + " " + str(item_data.it_position) + " " + str(item_data.it_respawn_time) + "\n"
    
    def get_data(self) -> str:
        #has a trailing newline
        return self.data


class BLS_BrickPosVec3:
    #a special vec3 type for bricks in blockland
    #this was unfortunately initially based on some wrong assumptions, and some help properly deciphering coordinates in a savefile would be of great help
    #that said, it still for the most part works for single brick types
    def __init__(self, x: float, y: float, z: float) -> None:
        self.x = float(round(x/2, 2))
        self.y = float(round(y/2, 2))
        self.z = float(round(z/5, 1))


class BLS_BrickShapeVec3:
    #defines a bricks' shape. a 1x1x1 brick is 1x1x3 on this scale
    #z is equivalent to plate height
    def __init__(self, x: int, y: int, z: int) -> None:
        self.x = x
        self.y = y
        self.z = z
            

class BLS_Brick:
    #defines a full brick and its' additional data in a .bls file
    def __init__(self, *, 
                 brick_shape: BLS_BrickShapeVec3,
                 brick_ui_name: str, 
                 position: BLS_BrickPosVec3 = BLS_BrickPosVec3(0,0,0), 
                 angle_id: int = 0, 
                 is_baseplate: int = 0, 
                 color_id: int = 1, 
                 print_id: str = "", 
                 color_fx_id: int = 0, 
                 shape_fx_id: int = 0, 
                 raycasting: int = 1, 
                 colliding:  int = 1, 
                 rendering:  int = 1, 
                 brick_data: BLS_BrickData | None = None) -> None:
        
        assert brick_shape != None, "Brick shape required"
        assert brick_ui_name != None, "Brick UI name required"
        assert position != None, "Brick position required"
        
        self.brick_shape = brick_shape
        
        self.__brick_name = brick_ui_name + "\""
        self.__brick_position = position
        self.__brick_angle = angle_id
        self.__brick_baseplate = is_baseplate
        self.__brick_color_id = color_id
        self.__brick_print_id = print_id
        self.__brick_color_fx_id = color_fx_id
        self.__brick_shape_fx_id = shape_fx_id
        self.__brick_raycasting = raycasting
        self.__brick_colliding = colliding
        self.__brick_rendering = rendering

        if brick_data == None:
            self.__brick_data = BLS_BrickData(BLS_BDFlags.OWNER)
        else:
            self.__brick_data = brick_data
            
    def set_pos(self, x: float, y: float, z: float) -> None:
        #sets the bricks' position manually
        pos = BLS_BrickPosVec3(self.brick_shape.x * x, self.brick_shape.y * y, self.brick_shape.z/2 + z)
        self.__brick_position = pos
        
    def set_pos_large(self, x: float, y: float, z: float, x_offset: float, y_offset: float) -> None:
        #sets the bricks' position manually
        #offsets a larger brick, first by shifting it over by half of its size, then by applying a manual offset
        #help with calculating this offset would be GREATLY APPRECIATED!
        pos = BLS_BrickPosVec3(self.brick_shape.x/2 * x, self.brick_shape.y/2 * y, self.brick_shape.z/2 + z)
        pos.x = pos.x + x_offset
        pos.y = pos.y + y_offset
        self.__brick_position = pos
    
    def get_brick(self) -> str:
        self.brick = "" + \
            self.__brick_name                           + " " + \
            str(f"{self.__brick_position.x:.2f}")       + " " + \
            str(f"{self.__brick_position.y:.2f}")       + " " + \
            str(f"{self.__brick_position.z:.1f}")       + " " + \
            str(self.__brick_angle)                     + " " + \
            str(self.__brick_baseplate)                 + " " + \
            str(self.__brick_color_id)                  + " " + \
            self.__brick_print_id                       + " " + \
            str(self.__brick_color_fx_id)               + " " + \
            str(self.__brick_shape_fx_id)               + " " + \
            str(self.__brick_raycasting)                + " " + \
            str(self.__brick_colliding)                 + " " + \
            str(self.__brick_rendering)                 + "\n"
        
        if self.__brick_data != None:
            if isinstance(self.__brick_data, BLS_BrickData):
                self.brick += self.__brick_data.get_data()
            else:
                for br_data in self.__brick_data:
                    if isinstance(br_data, BLS_BrickData):
                        self.brick += br_data.get_data()
        return self.brick


class BLS_File:
    #defines a .bls save file
    #takes a list of bricks to write, the colorset to use and the hardcoded header
    def __init__(self, bricks: list[BLS_Brick] | None = None, brick_count: int = 0, colorset: BLS_ColorSet = None) -> None:
        self.bricks = bricks
        self.brick_count = brick_count
        self.data: str = \
            BLS_HEADER_WARNING + "\n" + \
            BLS_HEADER_DESCRIPTION + "\n" + \
            colorset.get_colorset() + \
            BLS_HEADER_LINECOUNT + str(self.brick_count) + "\n"
                
    def write(self, path: str) -> None:
        assert self.bricks != None, "self.bricks must be a non empty list!"
        
        with open(path, "w") as file:
            file.write(self.data)
            print(f"Header done, ready to write {self.brick_count} bricks...")
            for brick in self.bricks:
                file.write(brick)
                