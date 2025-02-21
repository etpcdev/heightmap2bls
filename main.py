import sys

from PySide6.QtWidgets import QApplication, QMainWindow, QGraphicsScene, QGraphicsPixmapItem, QFileDialog
from PySide6.QtGui import QPixmap
from PySide6.QtCore import Qt
from gui.main_gui import Ui_MainWindow
from pathlib import Path
from platformdirs import user_pictures_path

import hm2bls as hm


class hm2bls(QMainWindow):
    def __init__(self, cm: Path, cs: Path, bricks: Path, out: Path, pictures: Path):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        
        self.__heightmap = ""
        self.__colormap  = str(cm)
        self.__colorset  = str(cs)
        self.__bricks    = str(bricks)
        self.__out       = str(out)
        
        # Gets platform appropriate path for Pictures directory
        self.__pictures  = str(pictures)
        
        # Set up defaults (to avoid hardcoding them into the UI)
        self.ui.line_cs.setText(self.__colorset)
        self.ui.line_brick.setText(self.__bricks)
        
        self.ui.sb_x.setValue(100)
        self.ui.sb_y.setValue(100)
        self.ui.sb_z.setValue(30)
        self.ui.sb_step.setValue(1)
        self.ui.sb_blid.setValue(-1)
        
        
        # Set up default image for color map
        self.scene_cm = QGraphicsScene(self)
        self.ui.gv_cm.setScene(self.scene_cm)
        
        self.pixmap_cm = QPixmap(self.__colormap)
        self.img_cm    = QGraphicsPixmapItem(self.pixmap_cm)
        self.scene_cm.addItem(self.img_cm)
        
        # Set up default image for height map (uses color map by default as it's blank)
        self.scene_hm = QGraphicsScene(self)
        self.ui.gv_hm.setScene(self.scene_hm)
        
        self.pixmap_hm = QPixmap(self.__colormap)
        self.img_hm    = QGraphicsPixmapItem(self.pixmap_hm)
        self.scene_hm.addItem(self.img_hm)
                
        
        # Signals
        self.ui.but_generate.clicked.connect(self.start_generation)
        
        self.ui.but_hm.clicked.connect(self.select_hm)
        self.ui.but_cm.clicked.connect(self.select_cm)
        
        self.ui.but_cs.clicked.connect(self.select_cs)
        self.ui.but_brick.clicked.connect(self.select_bricks)
        
        self.ui.gv_cm.resizeEvent = self.resizeEvent
        self.rescale_img()
    
    
    def select_hm(self):       
        file_path, _ = QFileDialog.getOpenFileName(self, "Select an image", self.__pictures, "Images (*.png *.jpg *.jpeg *.bmp *.webp)")
        
        if file_path:
            self.__heightmap = file_path
            
            self.scene_hm = QGraphicsScene(self)
            self.ui.gv_hm.setScene(self.scene_hm)
            
            self.pixmap_hm = QPixmap(self.__heightmap)
            self.img_hm    = QGraphicsPixmapItem(self.pixmap_hm)
            self.scene_hm.addItem(self.img_hm)
            
            self.rescale_img()
    
    
    def select_cm(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Select an image", self.__pictures, "Images (*.png *.jpg *.jpeg *.bmp *.webp)")
        
        if file_path:
            self.__colormap = file_path
            
            self.scene_cm = QGraphicsScene(self)
            self.ui.gv_cm.setScene(self.scene_cm)
            
            self.pixmap_cm = QPixmap(self.__colormap)
            self.img_cm    = QGraphicsPixmapItem(self.pixmap_cm)
            self.scene_cm.addItem(self.img_cm)
            
            self.rescale_img()
    
    
    def select_cs(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Select an colorset", "./res", "Colorset (*.txt)")
        
        if file_path:
            self.__colorset = file_path
            
            self.ui.line_cs.setText(file_path)
    
    
    def select_bricks(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Select an brick file", "./res", "Bricks (*.json)")
        
        if file_path:
            self.__bricks = file_path
            
            self.ui.line_brick.setText(file_path)
    
    
    def rescale_img(self):
        # Resize the images to fit their views
        size_cm = self.ui.gv_cm.size()
        size_hm = self.ui.gv_hm.size()
        
        pixmap_scaled_cm = self.pixmap_cm.scaled(size_cm.width(), 
                                                 size_cm.height(), 
                                                 Qt.AspectRatioMode.KeepAspectRatio, 
                                                 Qt.TransformationMode.SmoothTransformation)
        
        pixmap_scaled_hm = self.pixmap_hm.scaled(size_hm.width(), 
                                                 size_hm.height(), 
                                                 Qt.AspectRatioMode.KeepAspectRatio, 
                                                 Qt.TransformationMode.SmoothTransformation)
    
        self.img_cm.setPixmap(pixmap_scaled_cm)
        self.img_hm.setPixmap(pixmap_scaled_hm)
        
        self.img_cm.setPos(0, 0)
        self.img_hm.setPos(0, 0)
        
        
    def resizeEvent(self, event):
        # Hook into / override the resize event to make sure the images resize dynamically
        self.rescale_img()
        super().resizeEvent(event)
        
        
    def start_generation(self):
        file_path, _ = QFileDialog.getSaveFileName(self, "Select a location to save to", "./out")
        
        if not file_path:
            return
        
        # Get params
        heightmap = self.__heightmap
        x = str(self.ui.sb_x.value())
        y = str(self.ui.sb_y.value())
        z = str(self.ui.sb_z.value())
        colormap = self.__colormap
        colorset = self.__colorset
        bricks   = self.__bricks
        output   = file_path
        step     = self.ui.sb_step.value()
        blid     = self.ui.sb_blid.value()
        ground   = self.ui.cb_ground.isEnabled()
        gapfill  = self.ui.cb_gapfill.isEnabled()
        optimize = self.ui.cb_optimize.isEnabled()
        
        
        # Load and resize the height map
        height_map = hm.load_heightmap(heightmap, x, y)
        
        # Load and resize colormap == heightmap
        hm_x = height_map.shape[0]
        hm_y = height_map.shape[1]
        color_map = hm.load_colormap(colormap, hm_x, hm_y)
        
        # Load colorset
        color_set = hm.BLS_ColorSet(path=colorset)

        # Map colorset
        color_map = color_set.map_colors(color_map=color_map)

        # Resize z axis
        height_map = hm.resize_z(height_map, z)

        # Clamp z axis to step
        height_map = hm.clamp_step(height_map, step)
        
        # Sit map on the ground
        if ground:
            height_map = hm.ground(height_map)

        # Load brick file
        brick_file = hm.Bricks(bricks)
        
        # Set up map
        map = hm.MapGenerator(bricks=brick_file, height_map=height_map, 
                            color_map=color_map, bl_id=blid, 
                            color_set=color_set, output_path=output)
        map.setup_map()
        
        # Gapfill
        if gapfill:
            map.gap_fill()
        
        # Brick optimization
        if optimize:
            map.optimize()
            
        # Create save file
        map.create_save()


def main():
    # Set up default paths
    script_dir      = Path(__file__).parent.resolve()
    path_def_cm     = script_dir / "res" / "default" / "colorMap.png"
    path_def_cs     = script_dir / "res" / "default" / "colorSet.txt"
    path_def_bricks = script_dir / "res" / "default" / "defaultBricks.json"
    path_def_out    = script_dir / "out" / "map.bls"

    path_usr_pictures = user_pictures_path()

    app = QApplication(sys.argv)
    window = hm2bls(path_def_cm, path_def_cs, path_def_bricks, path_def_out, path_usr_pictures)
    window.show()
    sys.exit(app.exec())

        
if __name__ == "__main__":
    main()
    