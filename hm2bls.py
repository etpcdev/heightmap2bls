import argparse
import time
import hm2bls as hm

from pathlib import Path

def time_func(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        res = func(*args, **kwargs)
        end_time = time.time()
        exec_time = end_time - start_time
        print(f"[Map created in {exec_time:.4f} seconds]")
        return res
    return wrapper


@time_func
def main():
    #Set up default paths
    script_dir      = Path(__file__).parent.resolve()
    path_def_cm     = script_dir / "res" / "default" / "colorMap.png"
    path_def_cs     = script_dir / "res" / "default" / "colorSet.txt"
    path_def_bricks = script_dir / "res" / "default" / "defaultBricks.json"
    path_def_out    = script_dir / "out" / "map.bls"
    
    
    parser = argparse.ArgumentParser(prog="hm2bls", description="Convert heightmaps and color maps into .bls files.")
    parser.add_argument("-hm", "--heightmap", required=True, help="heightmap file to use.")
    parser.add_argument("-cm", "--colormap", default=path_def_cm, help="colormap file to use.")
    parser.add_argument("-cs", "--colorset", default=path_def_cs, help="colorset file to use.")
    parser.add_argument("-o", "--output", default=path_def_out, help="output file name.")
    parser.add_argument("-x", default=None, help="define x axis size.")
    parser.add_argument("-y", default=None, help="define y axis size.")
    parser.add_argument("-z", default=None, help="adjust the height from the lowest point.")
    parser.add_argument("--blid", default="999999", help="set the BL_ID to save the map under.")
    parser.add_argument("--ground", default=False, action="store_true", help="sit the map on the ground at it's lowest point.")
    parser.add_argument("--gapfill", default=False, action="store_true", help="fill steep vertical gaps.")
    parser.add_argument("--optimize", default=False, action="store_true", help="attempts to optimize the brickcount by using the second brick from a file.")
    parser.add_argument("--bricks", default=path_def_bricks, help="select the file that defines which bricks to use.")
    parser.add_argument("--step", default="1", help="define the vertical step of the map. (1 = plate, 3 = brick)")
    
    args = parser.parse_args()
    
    #Display settings used
    print(f"Generating \"{args.output}\" with settings:")
    print(f" [+]Heightmap:\t{args.heightmap}")
    print(f" [+]Colormap:\t{args.colormap}")
    print(f" [+]Colorset:\t{args.colorset}")
    print(f" [+]Output:\t{args.output}")
    print(f" [+]X size:\t{args.x}")
    print(f" [+]Y size:\t{args.y}")
    print(f" [+]Z size:\t{args.z}")
    print(f" [+]BL_ID:\t{args.blid}")
    print(f" [+]Ground:\t{args.ground}")
    print(f" [+]Gapfill:\t{args.gapfill}")
    print(f" [+]Brick File:\t{args.bricks}")
    print(f" [+]Step:\t{args.step}")
    
    #load and resize the height map and color map
    print(f"Loading height map \"{args.heightmap}\"...")
    start_time = time.time()
    height_map = hm.load_heightmap(args.heightmap, args.x, args.y)
    end_time = time.time()
    exec_time = end_time - start_time
    print(f"\t[+]Finished in {exec_time:.4f} seconds")
    
    hm_x = height_map.shape[0]
    hm_y = height_map.shape[1]
    
    print(f"Loading color map \"{args.colormap}\"...")
    start_time = time.time()
    color_map = hm.load_colormap(args.colormap, hm_x, hm_y)
    end_time = time.time()
    exec_time = end_time - start_time
    print(f"\t[+]Finished in {exec_time:.4f} seconds")
    
    print(f"Loading colorset \"{args.colorset}\"...")
    start_time = time.time()
    color_set = hm.BLS_ColorSet(path=args.colorset)
    end_time = time.time()
    exec_time = end_time - start_time
    print(f"\t[+]Finished in {exec_time:.4f} seconds")

    print(f"Mapping colorset...")
    start_time = time.time()
    color_map = color_set.map_colors(color_map=color_map)
    end_time = time.time()
    exec_time = end_time - start_time
    print(f"\t[+]Finished in {exec_time:.4f} seconds")

    if args.z:
        print(f"Resizing z axis to {args.z}...")
        start_time = time.time()
        height_map = hm.resize_z(height_map, args.z)
        end_time = time.time()
        exec_time = end_time - start_time
        print(f"\t[+]Finished in {exec_time:.4f} seconds")

    if args.step != "1":
        print(f"Clamping z axis to step {args.step}...")
        start_time = time.time()
        height_map = hm.clamp_step(height_map, args.step)
        end_time = time.time()
        exec_time = end_time - start_time
        print(f"\t[+]Finished in {exec_time:.4f} seconds")
    
    if args.ground:
        print(f"Grounding map...")
        start_time = time.time()
        height_map = hm.ground(height_map)
        end_time = time.time()
        exec_time = end_time - start_time
        print(f"\t[+]Finished in {exec_time:.4f} seconds")

    print(f"Loading brick file \"{args.bricks}\"...")
    start_time = time.time()
    bricks = hm.Bricks(args.bricks)
    end_time = time.time()
    exec_time = end_time - start_time
    print(f"\t[+]Finished in {exec_time:.4f} seconds")
    
    print(f"Setting up map...")
    start_time = time.time()
    map = hm.MapGenerator(bricks=bricks, height_map=height_map, color_map=color_map, bl_id=args.blid, color_set=color_set, output_path=args.output)
    map.setup_map()
    end_time = time.time()
    exec_time = end_time - start_time
    print(f"\t[+]Finished in {exec_time:.4f} seconds")
    
    
    if args.gapfill:
        print(f"Filling gaps...")
        start_time = time.time()
        map.gap_fill()
        end_time = time.time()
        exec_time = end_time - start_time
        print(f"\t[+]Finished in {exec_time:.4f} seconds")
    
    if args.optimize:
        print(f"Optimizing bricks...")
        start_time = time.time()
        map.optimize()
        end_time = time.time()
        exec_time = end_time - start_time
        print(f"\t[+]Finished in {exec_time:.4f} seconds")
        
    print(f"Creating .bls file \"{args.output}\"...")
    start_time = time.time()
    map.create_save()
    end_time = time.time()
    exec_time = end_time - start_time
    print(f"\t[+]Finished in {exec_time:.4f} seconds")
    
    
if __name__ == '__main__':
    main()