import sys
from ultralytics import YOLO
from subprocess import Popen

from PyQt5 import uic
from PyQt5.QtMultimedia import QCameraInfo
from PyQt5.QtWidgets import QMainWindow, QApplication


class MainWindow(QMainWindow):
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
      self.index = self.comboBox.currentIndex()
      Popen('python naebalovo.py')
      model = YOLO("models/yolo/yolov8n-pose.pt")
      results = model(source=self.index, show=True, conf=0.3, save=True)  # predict on an imagae


if __name__ == '__main__':
   app = QApplication(sys.argv)
   form = MainWindow()
   form.show()
   sys.exit(app.exec_())