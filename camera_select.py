import sys
from PyQt5 import uic
from PyQt5.QtMultimedia import QCameraInfo
from PyQt5.QtWidgets import QMainWindow, QApplication

from subprocess import Popen


class MainWindow(QMainWindow):
   print(1)
   def __init__(self):
      super().__init__()
      uic.loadUi('ui files/select_cameras.ui', self)
      self.available_cameras = QCameraInfo.availableCameras()
      if not self.available_cameras:
         sys.exit()
      self.comboBox.addItems([camera.description() for camera in self.available_cameras])
      print("Готов к использованию")
      self.pushButton.clicked.connect(self.camera_active)

   def camera_active(self):
      Popen('python face.py')

app = QApplication(sys.argv)
form = MainWindow()
form.show()
sys.exit(app.exec_())