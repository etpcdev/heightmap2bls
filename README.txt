Thank you for using hm2bls (heightmap2bls)!

Requirements
    Python 3.11+ (Earlier versions might work but are untested)
    pip

Setup instructions
{For Windows Users :: Make sure Python is installed to PATH.}

    Windows: 
        python -m pip install -r requirements.txt

    Linux/MacOS:
        pip install -r requirements.txt

Usage instructions
There is only one mandatory argument, to select a heightmap as the program does not come packaged with a default heightmap.
You will have to source your own.

    Windows:
        python hm2bls.py -hm [path to a height map] ... [args]
    
    Linux/MacOS:
        python3 hm2bls.py -hm [path to a height map] ... [args]

    By default, the program will output the .bls file to the "out" folder, as "map.bls".
    
Below is the full list of arguments and options.
################################################

usage: hm2bls [-h] -hm HEIGHTMAP [-cm COLORMAP] [-cs COLORSET] [-o OUTPUT] [-x X] [-y Y] [-z Z] [--blid BLID] [--ground] [--gapfill] [--optimize] [--bricks BRICKS] [--step STEP]

Convert heightmaps and color maps into .bls files.

options:
  -h, --help            show this help message and exit
  -hm HEIGHTMAP, --heightmap HEIGHTMAP
                        heightmap file to use.
  -cm COLORMAP, --colormap COLORMAP
                        colormap file to use.
  -cs COLORSET, --colorset COLORSET
                        colorset file to use.
  -o OUTPUT, --output OUTPUT
                        output file name.
  -x X                  define x axis size.
  -y Y                  define y axis size.
  -z Z                  adjust the height from the lowest point.
  --blid BLID           set the BL_ID to save the map under.
  --ground              sit the map on the ground at it's lowest point.
  --gapfill             fill steep vertical gaps.
  --optimize            attempts to optimize the brickcount by using the second brick from a file.
  --bricks BRICKS       select the file that defines which bricks to use.
  --step STEP           define the vertical step of the map. (1 = plate, 3 = brick)

################################################
#             ABOUT THE BRICK FILES            #
################################################

They must follow the json format given in the template.
"ui_name" must be identical to the name of the brick in game.
"shape":[x,y,z] defines the size of the brick. The z size is measured in plates.
"offset":[x,y]  defines how much to offset the brick by. This is only used for the second brick when the --optimize flag is enabled.
                Because of limited understanding of how the .bls handles coordinates properly, you must experiment with the offset manually.

                For now, the other options are not really used and are just there as provisions for possible future changes.

                The second brick in the json file is the "optimization" brick. It should be 2x the first brick's width and length, 
                but must be the same height, otherwise things will not generate properly.

                The terrainBricks.json file requires the mini terrain addon by goldtits (Brick_4n8brickH.zip).
                    [MERP United discord server: https://discord.gg/EfQ22KGH8t]
                    [Direct download: https://cdn.discordapp.com/attachments/525811965398876160/1055599397880201246/Brick_4n8brickH.zip?ex=67765dcc&is=67750c4c&hm=2faa96e7b56fe64d7638e380e1d385a6d0cc88e5f749c63d2f2e8854de5e2214&]

Height maps must use 8bit color. (8bit rgba)
Contact me @ etpcdev@gmail.com
