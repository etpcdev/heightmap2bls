from .maps import load_heightmap, load_colormap, resize_z, clamp_step, ground
from .blsutils import *

import json

class Bricks:
    #loads the bricks to use from a json file
    def __init__(self, path: str | None = None) -> None:
        assert path != None, "Invalid brick file."

        try: file = open(path, "r")
        
        except FileNotFoundError:
            print(f"File \"{path}\" not found\nExiting...")
            quit(code=1)
        
        else:
            with file:
                try:
                    self.brick_data = dict(json.load(file))
                except json.JSONDecodeError as e:
                    print(e)
                    print(f"Failed to parse JSON data in \"{path}\".\nCheck formatting.\nExiting...")
                    quit(code=1)
        

class MapGenerator:
    def __init__(self,*, bricks: Bricks, 
                 height_map: np.ndarray, 
                 color_map: np.ndarray,
                 bl_id: str | None = None,
                 color_set: BLS_ColorSet,
                 output_path: str
                 ) -> None:
        assert bl_id != None, "Please provide a BL_ID."
        
        self.__bricks = bricks
        self.__hm = height_map
        self.__cm = color_map
        self.__map = np.zeros(shape=(height_map.shape[0], height_map.shape[1]), dtype=object)
        self.__bl_id = bl_id
        self.__color_set = color_set
        self.__output_path = output_path
        
    def gap_fill(self) -> None:
        #check all four sides (if possible) for gaps
        #then gets the largest gap and sets the brick's gap count to the amount of bricks needed to fill
        brick_height = self.__bricks.brick_data["bricks"][0]["shape"][2]

        for i in range(0, len(self.__hm)):
            for j in range(0, len(self.__hm[i])):
                largest_gap = 0
                
                if i > 0:
                    if self.__hm[i][j] > self.__hm[i-1][j]:
                        gap = self.__hm[i][j] - self.__hm[i-1][j]
                        if gap > brick_height:
                            bricks_per_gap = math.ceil(gap / brick_height)
                            if bricks_per_gap > largest_gap:
                                largest_gap = bricks_per_gap
                    
                if i < len(self.__hm)-1:
                    if self.__hm[i][j] > self.__hm[i+1][j]:
                        gap = self.__hm[i][j] - self.__hm[i+1][j]
                        if gap > brick_height:
                            bricks_per_gap = math.ceil(gap / brick_height)
                            if bricks_per_gap > largest_gap:
                                largest_gap = bricks_per_gap
                 
                if j > 0:
                    if self.__hm[i][j] > self.__hm[i][j-1]:
                        gap = self.__hm[i][j] - self.__hm[i][j-1]
                        if gap > brick_height:
                            bricks_per_gap = math.ceil(gap / brick_height)
                            if bricks_per_gap > largest_gap:
                                largest_gap = bricks_per_gap
                
                if j < len(self.__hm[i])-1:
                    if self.__hm[i][j] > self.__hm[i][j+1]:
                        gap = self.__hm[i][j] - self.__hm[i][j+1]
                        if gap > brick_height:
                            bricks_per_gap = math.ceil(gap / brick_height)
                            if bricks_per_gap > largest_gap:
                                largest_gap = bricks_per_gap

                if largest_gap > 0:
                    self.__map[i][j][3] = largest_gap

    
    def optimize(self) -> None:
        #tries to optimise brickcount by annulling adjacent bricks of the same height and color up to a 2x2 grid
        seen = []
        for i in range(len(self.__map)-1):
            for j in range(len(self.__map[i])-1):
                #skip if the unique index has been seen before, or if the unique index of the next brick has been seen (to avoid corner clipping)
                if self.__map[i][j][2] in seen or self.__map[i][j+1][2] in seen:
                    continue
                else:
                    seen.append(self.__map[i][j][2])
                    if len({self.__map[i][j][0], self.__map[i+1][j][0], self.__map[i][j+1][0], self.__map[i+1][j+1][0]}) == 1 and \
                       len({self.__map[i][j][1], self.__map[i+1][j][1], self.__map[i][j+1][1], self.__map[i+1][j+1][1]}) == 1:
                        
                        #set unique IDs to the same ID (as they will ultimately become one brick)
                        self.__map[i+1][j][2]   = self.__map[i][j][2]
                        self.__map[i][j+1][2]   = self.__map[i][j][2]
                        self.__map[i+1][j+1][2] = self.__map[i][j][2]

                        #fill vertical gaps for optimized bricks
                        largest_gap = max(self.__map[i][j][3], self.__map[i+1][j][3], self.__map[i][j+1][3], self.__map[i+1][j+1][3])
                        self.__map[i][j][3]     = largest_gap
                        self.__map[i+1][j][3]   = largest_gap
                        self.__map[i][j+1][3]   = largest_gap
                        self.__map[i+1][j+1][3] = largest_gap
                        
                        #set brick to use brick type 2
                        self.__map[i][j][4]     = 1
                        self.__map[i+1][j][4]   = 1
                        self.__map[i][j+1][4]   = 1
                        self.__map[i+1][j+1][4] = 1
    
    def setup_map(self) -> None:
        #creates a map containing useful data
        # self.__map[i][j]:
        # -> height
        # -> colorset mapping
        # -> unique brick index
        # -> vertical stack count (for gap_fill)
        # -> brick type to use (default is 0, the smaller brick)
        
        unique_brick_index = 0
        
        for i in range(0, len(self.__map)):
            for j in range(0, len(self.__map[0])):
                self.__map[i][j] = [int(self.__hm[i][j]), int(self.__cm[i][j]), unique_brick_index, 1, 0]
                unique_brick_index += 1     
        
    def __make_brick(self, index: int, color: int) -> BLS_Brick:
        #creates a brick using info from the brick file and CLI args
        shape = BLS_BrickShapeVec3(*self.__bricks.brick_data["bricks"][index]["shape"])
        ui_name = self.__bricks.brick_data["bricks"][index]["ui_name"]
        owner_data = BLS_OwnerData(int(self.__bl_id))
        brick_data = BLS_BrickData(BLS_BDFlags.OWNER, owner_data=owner_data)
        return BLS_Brick(brick_shape=shape, brick_ui_name=ui_name, color_id=color, brick_data=brick_data)
    
    def create_save(self) -> None:
        #makes a list of all the bricks to be used in the save and hands it to the BLS_File handler
        seen = []
        bricks = []
        brick_height = self.__bricks.brick_data["bricks"][0]["shape"][2]
        
        for i in range(0, len(self.__map)):
            for j in range(0, len(self.__map[i])):
                if self.__map[i][j][2] in seen:
                    continue
                else:
                    while self.__map[i][j][3] > 0:
                        seen.append(self.__map[i][j][2])
                        out_brick = self.__make_brick(self.__map[i][j][4], self.__map[i][j][1])
                        
                        #choose the brick to use (only applicable if --optimize arg is used)
                        new_z = (self.__map[i][j][0]-((self.__map[i][j][3] - 1) * brick_height))
                        if self.__map[i][j][4] == 0:
                            out_brick.set_pos(i, j, new_z)    
                        else:                          
                            x_offset = self.__bricks.brick_data["bricks"][1]["offset"][0]
                            y_offset = self.__bricks.brick_data["bricks"][1]["offset"][1]
                            out_brick.set_pos_large(i, j, new_z, x_offset, y_offset)
                            
                        bricks.append(out_brick)
                        self.__map[i][j][3]-=1
        
        save_file = BLS_File(bricks, self.__color_set)
        save_file.write(self.__output_path)
        
