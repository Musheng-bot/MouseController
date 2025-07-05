from PyQt5.QtWidgets import QWidget
from MouseController import MouseController
from AppBase import QtFactory, SharedApp

class RecordWidget(QWidget):
    def __init__(self, parent=None):
        super(RecordWidget, self).__init__(parent)
        self.app = SharedApp.get_app()
