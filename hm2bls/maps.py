from PIL import Image
import numpy as np


def load_heightmap(path: str, x: str | None, y: str | None) -> np.ndarray:
    #loads an image to be used as a height map and forcibly adds an alpha channel if it doesn't have one
    #rescales the map according to the cli args -x and -y
    with Image.open(path) as img:
        img = img.convert("RGBA")
        height_map: np.ndarray = np.array(img, dtype=np.uint8)
        
        resize = False
        new_size = []
        
        if x == None:
            x = height_map.shape[1]
        if y == None:
            y = height_map.shape[0]
        
        
        if y != height_map.shape[0]:
            new_size.append(int(y))
            resize = True
        else:
            new_size.append(height_map.shape[0])
        
        if x != height_map.shape[1]:
            new_size.append(int(x))
            resize = True
        else:
            new_size.append(height_map.shape[1])
        
        if resize:
            new_size = tuple(new_size)
            height_map = Image.fromarray(height_map).resize(new_size, Image.Resampling.BICUBIC)
            height_map = np.array(height_map)
            
        #squash the grayscale height map into a 2d array
        height_map = height_map[:, :, :1].astype(np.uint32).squeeze(axis=2)
    return height_map

def load_colormap(path: str, x: str | None, y: str | None) -> np.ndarray:
    #does the same as above but keeps rgba data
    #rescales the map according to the cli args -x and -y
    with Image.open(path) as img:
        img = img.convert("RGBA")
        color_map: np.ndarray = np.array(img, dtype=np.uint8)
    
        resize = False
        new_size = []
        
        if x == None:
            x = color_map.shape[1]
        if y == None:
            y = color_map.shape[0]
        
        
        if y != color_map.shape[0]:
            new_size.append(int(y))
            resize = True
        else:
            new_size.append(color_map.shape[0])
        
        if x != color_map.shape[1]:
            new_size.append(int(x))
            resize = True
        else:
            new_size.append(color_map.shape[1])
        
        if resize:
            new_size = tuple(new_size)
            color_map = Image.fromarray(color_map).resize(new_size, Image.Resampling.BICUBIC)
            color_map = np.array(color_map)
            
    return color_map

def resize_z(height_map: np.ndarray[np.uint32], z: str) -> np.ndarray:
    #stretches the heightmap to z flat bricks 
    min_val = height_map.min()
    max_val = height_map.max()
    z = int(z)
    
    if max_val == min_val:
        return height_map.copy()
    
    if max_val == 0: 
        return np.zeros_like(height_map, dtype=np.uint32)
    
    #this should preserve the minimum height and stretch the other values to fit into z + min height
    height_map = min_val + ((height_map - min_val)/(max_val - min_val) * (z))
    
    return height_map.astype(np.uint32)

def clamp_step(height_map: np.ndarray[np.uint32], step: str) -> np.ndarray:
    #clamps the map to the nearest step
    step = int(step)
    height_map = np.round(height_map / step) * step
    
    return height_map.astype(np.uint32)

def ground(height_map: np.ndarray[np.uint32]) -> np.ndarray:
    #lowers the map to the ground if it isn't already
    min_val = height_map.min()
    height_map = (height_map - min_val)
    return height_map.astype(np.uint32)