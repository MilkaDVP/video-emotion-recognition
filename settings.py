import sys
from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QApplication


class MainWindow(QMainWindow):
   def __init__(self):
      super().__init__()
      uic.loadUi('ui files/settings.ui', self)


if __name__ == '__main__':
   app = QApplication(sys.argv)
   form = MainWindow()
   form.setFixedSize(830, 270)
   form.setWindowTitle('Настройки')
   form.show()
   app.exec()