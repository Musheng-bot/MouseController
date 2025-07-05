# 本模块用于和用户交互的部分
import logging

from PyQt5.QtCore import QPoint, QObject, QSize
from PyQt5.QtGui import QKeySequence
from PyQt5.QtWidgets import QLineEdit, QButtonGroup

from App.MouseController import MouseController
from PyQt5 import QtCore, QtGui, QtWidgets


class Interaction(QtWidgets.QMainWindow):
    start_record_key = 'alt'
    stop_record_key = 'f2'
    stop_key = 'shift'
    start_control_key = 'ctrl'
    save_data_key = 'f6'
    load_data_key = 'f7'
    clear_data_key = 'f8'
    btn_size = QSize(200, 80)

    def __init__(self, parent=None):
        btn_size = Interaction.btn_size
        super(Interaction, self).__init__(parent)
        self.logger = logging.getLogger("Interaction")
        self.logger.setLevel(logging.INFO)
        self.logger.addHandler(logging.FileHandler('./Log/Interaction.log'))
        self.logger.formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

        self.logger.info("Initializing Interaction")
        self.resize(1600, 1600)

        self.application = MouseController()

        self.tool_btn_group = QButtonGroup(self)
        self.tool_btn_group.addButton(self.generate_tool_btn(self, "录制", QPoint(0,0), None, ))
        self.start_record_btn = Interaction.generate_push_button(parent=self,
                                                                 text="Start Record",
                                                                 location=QPoint(400, 200),
                                                                 slot_func=self.application.start_record,
                                                                 size=btn_size,
                                                                 short_cut=Interaction.start_record_key)
        self.stop_record_btn = Interaction.generate_push_button(parent=self,
                                                                text="Stop Record",
                                                                location=QPoint(400, 300),
                                                                slot_func=self.application.stop_record,
                                                                size=btn_size,
                                                                short_cut=Interaction.stop_record_key)
        self.save_data_btn = Interaction.generate_push_button(parent=self,
                                                              text="Save Data",
                                                              location=QPoint(400, 400),
                                                              slot_func=self.application.save_data,
                                                              size=btn_size,
                                                              short_cut=Interaction.save_data_key)
        self.load_data_btn = Interaction.generate_push_button(parent=self,
                                                              text="Load Data",
                                                              location=QPoint(400, 500),
                                                              slot_func=self.application.load_data,
                                                              size=btn_size,
                                                              short_cut=Interaction.load_data_key)
        self.clear_data_btn = Interaction.generate_push_button(parent=self,
                                                               text="Clear Data",
                                                               location=QPoint(400, 600),
                                                               slot_func=self.application.clear_data,
                                                               size=btn_size,
                                                               short_cut=Interaction.clear_data_key)
        self.start_control_key = Interaction.generate_push_button(parent=self,
                                                                  text="Start Control",
                                                                  location=QPoint(400, 700),
                                                                  slot_func=self.application.start_control,
                                                                  size=btn_size,
                                                                  short_cut=Interaction.start_control_key)
        self.stop_control_key = Interaction.generate_push_button(parent=self,
                                                                 text="Stop Control",
                                                                 location=QPoint(400, 800),
                                                                 slot_func=self.application.stop_control,
                                                                 size=btn_size,
                                                                 short_cut=Interaction.stop_key)
        self.QLineEdit = QLineEdit(self)
        self.QLineEdit.setPlaceholderText("Enter recording name")

