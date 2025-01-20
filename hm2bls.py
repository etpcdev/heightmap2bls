import argparse
import hm2bls as hm
from pathlib import Path


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
    print(f"Generating \"{args.output}\" with settings:\n",
          f"-> Heightmap:\t{args.heightmap}\n",
          f"-> Colormap:\t{args.colormap}\n",
          f"-> Colorset:\t{args.colorset}\n",
          f"-> Output:\t{args.output}\n",
          f"-> X size:\t{args.x}\n",
          f"-> Y size:\t{args.y}\n",
          f"-> Z size:\t{args.z}\n",
          f"-> BL_ID:\t{args.blid}\n",
          f"-> Ground:\t{args.ground}\n",
          f"-> Gapfill:\t{args.gapfill}\n",
          f"-> Brick File:\t{args.bricks}\n",
          f"-> Step:\t{args.step}\n")
    
    #load and resize the height map and color map
    print(f"Loading height map \"{args.heightmap}\"...")
    height_map = hm.load_heightmap(args.heightmap, args.x, args.y)
    
    #Resize colormap == heightmap
    hm_x = height_map.shape[0]
    hm_y = height_map.shape[1]
    print(f"Loading color map \"{args.colormap}\"...")
    color_map = hm.load_colormap(args.colormap, hm_x, hm_y)
    
    print(f"Loading colorset \"{args.colorset}\"...")
    color_set = hm.BLS_ColorSet(path=args.colorset)

    print(f"Mapping colorset...")
    color_map = color_set.map_colors(color_map=color_map)


    if args.z:
        print(f"Resizing z axis to {args.z}...")
        height_map = hm.resize_z(height_map, args.z)

    if args.step != "1":
        print(f"Clamping z axis to step {args.step}...")
        height_map = hm.clamp_step(height_map, args.step)
    
    if args.ground:
        print(f"Grounding map...")
        height_map = hm.ground(height_map)

    print(f"Loading brick file \"{args.bricks}\"...")
    bricks = hm.Bricks(args.bricks)
    
    print(f"Setting up map...")
    map = hm.MapGenerator(bricks=bricks, height_map=height_map, 
                          color_map=color_map, bl_id=args.blid, 
                          color_set=color_set, output_path=args.output)
    map.setup_map()
    
    
    if args.gapfill:
        print(f"Filling gaps...")
        map.gap_fill()
    
    if args.optimize:
        print(f"Optimizing bricks...")
        map.optimize()
        
    print(f"Creating .bls file \"{args.output}\"...")
    map.create_save()
    
    
if __name__ == '__main__':
    main()