# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'main_gui.ui'
##
## Created by: Qt User Interface Compiler version 6.8.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QCheckBox, QFrame, QGraphicsView,
    QGridLayout, QHBoxLayout, QLabel, QLineEdit,
    QMainWindow, QPushButton, QSizePolicy, QSpinBox,
    QVBoxLayout, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(800, 741)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayoutWidget_3 = QWidget(self.centralwidget)
        self.verticalLayoutWidget_3.setObjectName(u"verticalLayoutWidget_3")
        self.verticalLayoutWidget_3.setGeometry(QRect(19, 9, 761, 701))
        self.vlay_main = QVBoxLayout(self.verticalLayoutWidget_3)
        self.vlay_main.setObjectName(u"vlay_main")
        self.vlay_main.setContentsMargins(0, 0, 0, 0)
        self.hlay_maps = QHBoxLayout()
        self.hlay_maps.setObjectName(u"hlay_maps")
        self.vlay_hm = QVBoxLayout()
        self.vlay_hm.setObjectName(u"vlay_hm")
        self.lab_hm = QLabel(self.verticalLayoutWidget_3)
        self.lab_hm.setObjectName(u"lab_hm")

        self.vlay_hm.addWidget(self.lab_hm)

        self.but_hm = QPushButton(self.verticalLayoutWidget_3)
        self.but_hm.setObjectName(u"but_hm")

        self.vlay_hm.addWidget(self.but_hm)

        self.gv_hm = QGraphicsView(self.verticalLayoutWidget_3)
        self.gv_hm.setObjectName(u"gv_hm")

        self.vlay_hm.addWidget(self.gv_hm)


        self.hlay_maps.addLayout(self.vlay_hm)

        self.vlay_cm = QVBoxLayout()
        self.vlay_cm.setObjectName(u"vlay_cm")
        self.lab_cm = QLabel(self.verticalLayoutWidget_3)
        self.lab_cm.setObjectName(u"lab_cm")

        self.vlay_cm.addWidget(self.lab_cm)

        self.but_cm = QPushButton(self.verticalLayoutWidget_3)
        self.but_cm.setObjectName(u"but_cm")

        self.vlay_cm.addWidget(self.but_cm)

        self.gv_cm = QGraphicsView(self.verticalLayoutWidget_3)
        self.gv_cm.setObjectName(u"gv_cm")

        self.vlay_cm.addWidget(self.gv_cm)


        self.hlay_maps.addLayout(self.vlay_cm)


        self.vlay_main.addLayout(self.hlay_maps)

        self.line = QFrame(self.verticalLayoutWidget_3)
        self.line.setObjectName(u"line")
        self.line.setFrameShape(QFrame.Shape.HLine)
        self.line.setFrameShadow(QFrame.Shadow.Sunken)

        self.vlay_main.addWidget(self.line)

        self.lab_cs = QLabel(self.verticalLayoutWidget_3)
        self.lab_cs.setObjectName(u"lab_cs")

        self.vlay_main.addWidget(self.lab_cs)

        self.hlay_cs = QHBoxLayout()
        self.hlay_cs.setObjectName(u"hlay_cs")
        self.line_cs = QLineEdit(self.verticalLayoutWidget_3)
        self.line_cs.setObjectName(u"line_cs")

        self.hlay_cs.addWidget(self.line_cs)

        self.but_cs = QPushButton(self.verticalLayoutWidget_3)
        self.but_cs.setObjectName(u"but_cs")

        self.hlay_cs.addWidget(self.but_cs)


        self.vlay_main.addLayout(self.hlay_cs)

        self.lab_brick = QLabel(self.verticalLayoutWidget_3)
        self.lab_brick.setObjectName(u"lab_brick")

        self.vlay_main.addWidget(self.lab_brick)

        self.hlay_bricks = QHBoxLayout()
        self.hlay_bricks.setObjectName(u"hlay_bricks")
        self.line_brick = QLineEdit(self.verticalLayoutWidget_3)
        self.line_brick.setObjectName(u"line_brick")

        self.hlay_bricks.addWidget(self.line_brick)

        self.but_brick = QPushButton(self.verticalLayoutWidget_3)
        self.but_brick.setObjectName(u"but_brick")

        self.hlay_bricks.addWidget(self.but_brick)


        self.vlay_main.addLayout(self.hlay_bricks)

        self.line_2 = QFrame(self.verticalLayoutWidget_3)
        self.line_2.setObjectName(u"line_2")
        self.line_2.setFrameShape(QFrame.Shape.HLine)
        self.line_2.setFrameShadow(QFrame.Shadow.Sunken)

        self.vlay_main.addWidget(self.line_2)

        self.gridLayout_3 = QGridLayout()
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.vlay_xyz = QVBoxLayout()
        self.vlay_xyz.setObjectName(u"vlay_xyz")
        self.hlay_x = QHBoxLayout()
        self.hlay_x.setObjectName(u"hlay_x")
        self.label_10 = QLabel(self.verticalLayoutWidget_3)
        self.label_10.setObjectName(u"label_10")

        self.hlay_x.addWidget(self.label_10)

        self.sb_x = QSpinBox(self.verticalLayoutWidget_3)
        self.sb_x.setObjectName(u"sb_x")
        self.sb_x.setMaximum(999999999)

        self.hlay_x.addWidget(self.sb_x)


        self.vlay_xyz.addLayout(self.hlay_x)

        self.hlay_y = QHBoxLayout()
        self.hlay_y.setObjectName(u"hlay_y")
        self.label_11 = QLabel(self.verticalLayoutWidget_3)
        self.label_11.setObjectName(u"label_11")

        self.hlay_y.addWidget(self.label_11)

        self.sb_y = QSpinBox(self.verticalLayoutWidget_3)
        self.sb_y.setObjectName(u"sb_y")
        self.sb_y.setMaximum(999999999)

        self.hlay_y.addWidget(self.sb_y)


        self.vlay_xyz.addLayout(self.hlay_y)

        self.hlay_z = QHBoxLayout()
        self.hlay_z.setObjectName(u"hlay_z")
        self.label_12 = QLabel(self.verticalLayoutWidget_3)
        self.label_12.setObjectName(u"label_12")

        self.hlay_z.addWidget(self.label_12)

        self.sb_z = QSpinBox(self.verticalLayoutWidget_3)
        self.sb_z.setObjectName(u"sb_z")
        self.sb_z.setMaximum(999999999)

        self.hlay_z.addWidget(self.sb_z)


        self.vlay_xyz.addLayout(self.hlay_z)


        self.gridLayout_3.addLayout(self.vlay_xyz, 4, 0, 1, 1)

        self.cb_optimize = QCheckBox(self.verticalLayoutWidget_3)
        self.cb_optimize.setObjectName(u"cb_optimize")

        self.gridLayout_3.addWidget(self.cb_optimize, 2, 1, 1, 1)

        self.cb_gapfill = QCheckBox(self.verticalLayoutWidget_3)
        self.cb_gapfill.setObjectName(u"cb_gapfill")

        self.gridLayout_3.addWidget(self.cb_gapfill, 2, 0, 1, 1)

        self.lab_options = QLabel(self.verticalLayoutWidget_3)
        self.lab_options.setObjectName(u"lab_options")

        self.gridLayout_3.addWidget(self.lab_options, 1, 0, 1, 1)

        self.cb_ground = QCheckBox(self.verticalLayoutWidget_3)
        self.cb_ground.setObjectName(u"cb_ground")

        self.gridLayout_3.addWidget(self.cb_ground, 3, 0, 1, 1)

        self.vlay_step_blid = QVBoxLayout()
        self.vlay_step_blid.setObjectName(u"vlay_step_blid")
        self.hlay_step = QHBoxLayout()
        self.hlay_step.setObjectName(u"hlay_step")
        self.label_13 = QLabel(self.verticalLayoutWidget_3)
        self.label_13.setObjectName(u"label_13")

        self.hlay_step.addWidget(self.label_13)

        self.sb_step = QSpinBox(self.verticalLayoutWidget_3)
        self.sb_step.setObjectName(u"sb_step")
        self.sb_step.setMaximum(999999999)

        self.hlay_step.addWidget(self.sb_step)


        self.vlay_step_blid.addLayout(self.hlay_step)

        self.hlay_blid = QHBoxLayout()
        self.hlay_blid.setObjectName(u"hlay_blid")
        self.label_15 = QLabel(self.verticalLayoutWidget_3)
        self.label_15.setObjectName(u"label_15")

        self.hlay_blid.addWidget(self.label_15)

        self.sb_blid = QSpinBox(self.verticalLayoutWidget_3)
        self.sb_blid.setObjectName(u"sb_blid")
        self.sb_blid.setMinimum(-1)
        self.sb_blid.setMaximum(999999999)

        self.hlay_blid.addWidget(self.sb_blid)


        self.vlay_step_blid.addLayout(self.hlay_blid)


        self.gridLayout_3.addLayout(self.vlay_step_blid, 4, 1, 1, 1)


        self.vlay_main.addLayout(self.gridLayout_3)

        self.but_generate = QPushButton(self.verticalLayoutWidget_3)
        self.but_generate.setObjectName(u"but_generate")

        self.vlay_main.addWidget(self.but_generate)

        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.lab_hm.setText(QCoreApplication.translate("MainWindow", u"Heightmap [Required]", None))
        self.but_hm.setText(QCoreApplication.translate("MainWindow", u"Select", None))
        self.lab_cm.setText(QCoreApplication.translate("MainWindow", u"Colormap [Optional]", None))
        self.but_cm.setText(QCoreApplication.translate("MainWindow", u"Select", None))
        self.lab_cs.setText(QCoreApplication.translate("MainWindow", u"Colorset [Optional]", None))
        self.but_cs.setText(QCoreApplication.translate("MainWindow", u"Select", None))
        self.lab_brick.setText(QCoreApplication.translate("MainWindow", u"Brick File [Optional]", None))
        self.but_brick.setText(QCoreApplication.translate("MainWindow", u"Select", None))
        self.label_10.setText(QCoreApplication.translate("MainWindow", u"X [Map Depth]", None))
        self.label_11.setText(QCoreApplication.translate("MainWindow", u"Y [Map Width]", None))
        self.label_12.setText(QCoreApplication.translate("MainWindow", u"Z [Map Height]", None))
        self.cb_optimize.setText(QCoreApplication.translate("MainWindow", u"Optimize Brickcount", None))
        self.cb_gapfill.setText(QCoreApplication.translate("MainWindow", u"Fill Vertical Gaps", None))
        self.lab_options.setText(QCoreApplication.translate("MainWindow", u"Options", None))
        self.cb_ground.setText(QCoreApplication.translate("MainWindow", u"Sit Map on the Ground", None))
        self.label_13.setText(QCoreApplication.translate("MainWindow", u"Step Clamp", None))
        self.label_15.setText(QCoreApplication.translate("MainWindow", u"BL_ID", None))
        self.but_generate.setText(QCoreApplication.translate("MainWindow", u"Generate", None))
    # retranslateUi

