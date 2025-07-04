# 本模块用于和用户交互的部分
import logging
from Application import Application
from PyQt5 import QtCore, QtGui, QtWidgets

class Interaction:
    def __init__(self):
        self.logger = logging.getLogger("Interaction")
        self.logger.setLevel(logging.INFO)
        self.logger.addHandler(logging.FileHandler('./Logs/Interaction.log'))
        self.logger.formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

        self.main_window = QtWidgets.QMainWindow()

        self.application = Application()


