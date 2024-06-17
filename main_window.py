import sys
from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QApplication


class MainWindow(QMainWindow):
   def __init__(self):
      super().__init__()
      uic.loadUi('ui files/main_window.ui', self)

      self.exit_button.clicked.connect(exit)
      self.camera_button.clicked.connect()
      self.setting.button.clicked.connect()

   def exit(self):
      sys.exit()


if __name__ == '__main__':
   app = QApplication(sys.argv)
   form = MainWindow()
   form.show()
   app.exec()