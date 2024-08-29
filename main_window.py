import sys
from subprocess import Popen
from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QApplication


class MainWindow(QMainWindow):
   def __init__(self):
      super().__init__()
      uic.loadUi('ui files/main_window.ui', self)

      self.exit_button.clicked.connect(self.exit)
      self.camera_button.clicked.connect(self.camera_capture)

   def exit(self):
      sys.exit()

   def camera_capture(self):
      Popen('python naebalovo.py')



if __name__ == '__main__':
   app = QApplication(sys.argv)
   form = MainWindow()
   form.show()
   app.exec()