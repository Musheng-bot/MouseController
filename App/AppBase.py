from PyQt5 import QtWidgets
from PyQt5.QtCore import QSize, QPoint

class QtFactory:
    @staticmethod
    def generate_push_button(parent, text: str, location: QPoint, slot_func, short_cut,
                             size: QSize = None) -> QtWidgets.QPushButton:
        button = QtWidgets.QPushButton(parent)
        button.clicked.connect(slot_func)
        button.setText(text)
        if size is not None:
            button.resize(size)
        else:
            button.adjustSize()
        button.move(location)
        button.setShortcut(short_cut)
        return button

    @staticmethod
    def generate_tool_btn(parent, text: str, location: QPoint, slot_func, size: QSize = None) -> QtWidgets.QToolButton:
        button = QtWidgets.QToolButton(parent)
        button.clicked.connect(slot_func)
        button.setText(text)
        if size is not None:
            button.resize(size)
        else:
            button.adjustSize()
        button.move(location)
        button.setAutoExclusive(True)
        return button

def singleton(cls):
    _instance = {}
    def inner():
        if cls not in _instance:
            _instance[cls] = cls()
        return _instance[cls]
    return inner
