import sys

from PyQt5.QtWidgets import QApplication, QMainWindow

from App.MouseController import MouseController
from App.Interaction import Interaction
from PyQt5 import QtCore, QtGui, QtWidgets


def main():
    app = QApplication(sys.argv)
    window = Interaction()
    window.show()
    return app.exec_()

def test():
    a = MouseController()
    b = MouseController()
    print(a is b)

if __name__ == '__main__':
    test()