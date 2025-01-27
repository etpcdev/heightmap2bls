from .maps import load_heightmap, load_colormap, resize_z, clamp_step, ground
from .blsutils import *
from .timer import timer
import json


class Bricks:
    # Must follow structure of brickTemplate.json
    brick_data: dict

    @timer
    def __init__(self, path: str) -> None:
    # Load brick definitions from json file
        path = str(path)
        
        if not path or not path.strip():
            raise ValueError("Invalid brick file path.")

        try:
            with open(path, "r") as file:
                self.brick_data = dict(json.load(file))
            
            if not isinstance(self.brick_data, dict):
                raise ValueError(f"The JSON data in \"{path}\" must be a valid JSON.")
        
        except FileNotFoundError:
            raise FileNotFoundError(f"File \"{path}\" not found.")
        
        except json.JSONDecodeError as e:
            raise ValueError(f"JSON parsing error in \"{path}\": {e}")
        

        

class MapGenerator:
    # Map elements:
    # [0] -> heightmap value
    # [1] -> color index
    # [2] -> unique brick index
    # [3] -> vertical brick count
    # [4] -> brick type (default is 0, the smaller brick)
    HEIGHT_INDEX = 0
    COLOR_INDEX  = 1
    UBID_INDEX   = 2
    VBC_INDEX    = 3
    BTYPE_INDEX  = 4
    
    def __init__(self,*, bricks: Bricks, 
                 height_map: np.ndarray, 
                 color_map: np.ndarray,
                 bl_id: str,
                 color_set: BLS_ColorSet,
                 output_path: str
                 ) -> None:
        
        if not isinstance(height_map, np.ndarray):
            raise TypeError("height_map must be a numpy array.")

        if height_map.shape != color_map.shape:
            raise ValueError("height_map and color_map must have the same shape.")

        if not str(output_path).strip():
            raise ValueError("output_path must be a non-empty string.")

        if not bl_id:
            raise ValueError("bl_id must be a non-empty string.")

        self.__bricks = bricks
        self.__hm = height_map
        self.__cm = color_map
        self.__map = np.zeros(shape=(height_map.shape[0], height_map.shape[1]), dtype=object)
        self.__bl_id = bl_id
        self.__color_set = color_set
        self.__output_path = output_path
    
    @timer
    def gap_fill(self) -> None:
        #Check adjacent bricks for vertical gaps
        #Calculate amount of bricks needed to fill gap
        
        brick_height = self.__bricks.brick_data["bricks"][0]["shape"][2]
        neighbor_offsets = [(-1,0),(1,0),(0,-1),(0,1)] #Up, down, left, right
        
        for i in range(0, len(self.__hm)):
            for j in range(0, len(self.__hm[i])):
                largest_gap = 0
                
                for offset_i, offset_j in neighbor_offsets:
                    new_i = i + offset_i
                    new_j = j + offset_j
                    
                    #Bounds check offsets
                    if 0 <= new_i < len(self.__hm) and 0 <= new_j < len(self.__hm[i]):
                        
                        if self.__hm[i][j] > self.__hm[new_i][new_j]:
                            gap = float(self.__hm[i][j]) - float(self.__hm[new_i][new_j])

                            if gap > brick_height:
                                bricks_per_gap = math.ceil(gap / brick_height)
                                largest_gap = max(largest_gap, bricks_per_gap)

                if largest_gap > 0:
                    self.__map[i][j][self.VBC_INDEX] = largest_gap

    @timer
    def optimize(self) -> None:
        #Tries to optimize brickcount by annulling adjacent bricks of the same height and color up to a 2x2 grid
        
        seen = set()
        for i in range(len(self.__map)-1):
            for j in range(len(self.__map[i])-1):
                #Skip seen index, including next brick (Avoid corner clipping)
                if self.__map[i][j][self.UBID_INDEX] in seen or self.__map[i][j+1][self.UBID_INDEX] in seen:
                    continue
                
                else:
                    seen.add(self.__map[i][j][self.UBID_INDEX])
                    if len({self.__map[i][j][self.HEIGHT_INDEX], self.__map[i+1][j][self.HEIGHT_INDEX], 
                            self.__map[i][j+1][self.HEIGHT_INDEX], self.__map[i+1][j+1][self.HEIGHT_INDEX]}) == 1 and \
                       len({self.__map[i][j][self.COLOR_INDEX], self.__map[i+1][j][self.COLOR_INDEX], 
                            self.__map[i][j+1][self.COLOR_INDEX], self.__map[i+1][j+1][self.COLOR_INDEX]}) == 1:
                        
                        #Overwrite unique index
                        self.__map[i+1][j][self.UBID_INDEX]   = self.__map[i][j][self.UBID_INDEX]
                        self.__map[i][j+1][self.UBID_INDEX]   = self.__map[i][j][self.UBID_INDEX]
                        self.__map[i+1][j+1][self.UBID_INDEX] = self.__map[i][j][self.UBID_INDEX]

                        #Overwrite vertical brick count
                        largest_gap = max(self.__map[i][j][self.VBC_INDEX], self.__map[i+1][j][self.VBC_INDEX], self.__map[i][j+1][self.VBC_INDEX], self.__map[i+1][j+1][self.VBC_INDEX])
                        self.__map[i][j][self.VBC_INDEX]     = largest_gap
                        self.__map[i+1][j][self.VBC_INDEX]   = largest_gap
                        self.__map[i][j+1][self.VBC_INDEX]   = largest_gap
                        self.__map[i+1][j+1][self.VBC_INDEX] = largest_gap
                        
                        #Overwrite brick type
                        self.__map[i][j][self.BTYPE_INDEX]     = 1
                        self.__map[i+1][j][self.BTYPE_INDEX]   = 1
                        self.__map[i][j+1][self.BTYPE_INDEX]   = 1
                        self.__map[i+1][j+1][self.BTYPE_INDEX] = 1
    
    @timer
    def setup_map(self) -> None:
        #creates a map containing useful data
        
                
        unique_brick_index = 0
        
        for i in range(0, len(self.__map)):
            for j in range(0, len(self.__map[i])):
                self.__map[i][j] = [int(self.__hm[i][j]), int(self.__cm[i][j]), unique_brick_index, 1, 0]
                unique_brick_index += 1
        
    def __make_brick(self, index: int, color: int) -> BLS_Brick:
        #Creates a brick using brick file data
        shape = BLS_BrickShapeVec3(*self.__bricks.brick_data["bricks"][index]["shape"])
        ui_name = self.__bricks.brick_data["bricks"][index]["ui_name"]
        
        if self.__bl_id != "-1":
            owner_data = BLS_OwnerData(int(self.__bl_id))
            brick_data = BLS_BrickData(BLS_BDFlags.OWNER, owner_data=owner_data)
        
        elif self.__bl_id == "-1":
            brick_data = BLS_BrickData()
        
        return BLS_Brick(brick_shape=shape, brick_ui_name=ui_name, color_id=color, brick_data=brick_data)
    
    @timer
    def create_save(self) -> None:
        #Make list of bricks to write
        seen = set()
        bricks = []
        brick_count = 0
        brick_height = self.__bricks.brick_data["bricks"][0]["shape"][2]
        
        #Manual offsets for large bricks
        x_offset = self.__bricks.brick_data["bricks"][1]["offset"][0]
        y_offset = self.__bricks.brick_data["bricks"][1]["offset"][1]
        
        for i in range(0, len(self.__map)):
            brick_row = ""
            
            for j in range(0, len(self.__map[i])):
                if self.__map[i][j][2] in seen:
                    continue
                
                else:
                    
                    for k in range(0, self.__map[i][j][self.VBC_INDEX]):
                        seen.add(self.__map[i][j][self.UBID_INDEX])
                        out_brick = self.__make_brick(self.__map[i][j][self.BTYPE_INDEX], self.__map[i][j][self.COLOR_INDEX])
                        
                        #Choose brick type
                        new_z = (self.__map[i][j][self.HEIGHT_INDEX]-((self.__map[i][j][self.VBC_INDEX] - 1) * brick_height))
                        if self.__map[i][j][self.BTYPE_INDEX] == 0:
                            out_brick.set_pos(i, j, new_z)  
                              
                        else:
                            out_brick.set_pos_large(i, j, new_z, x_offset, y_offset)
                            
                        brick_row += out_brick.get_brick()
                        brick_count += 1
                        self.__map[i][j][self.VBC_INDEX] -= 1
                        
            bricks.append(brick_row)
        
        save_file = BLS_File(bricks=bricks, brick_count=brick_count, colorset=self.__color_set)
        save_file.write(self.__output_path)
