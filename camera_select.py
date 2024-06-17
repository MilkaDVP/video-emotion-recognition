import os
import sys

import cv2
from PyQt5 import uic
from PyQt5.QtMultimedia import QCameraInfo, QCameraImageCapture, QCamera
from PyQt5.QtMultimediaWidgets import QCameraViewfinder
from PyQt5.QtWidgets import QMainWindow, QApplication


class MainWindow(QMainWindow):
   def __init__(self):
      super().__init__()
      uic.loadUi('ui files/select_cameras.ui', self)
      self.available_cameras = QCameraInfo.availableCameras()
      if not self.available_cameras:
         sys.exit()
      self.comboBox.addItems([camera.description() for camera in self.available_cameras])
      self.index = self.comboBox.currentIndex()
      print(self.index)
      self.pushButton.clicked.connect(self.camera_active)

   def camera_active(self):
      cap = cv2.VideoCapture(self.index)
      while True:
         ret, frame = cap.read()
         cv2.imshow('frame', frame)
         if cv2.waitKey(1) & 0xFF == ord('q'):
            break
      cap.release()


if __name__ == '__main__':
   app = QApplication(sys.argv)
   form = MainWindow()
   form.show()
   sys.exit(app.exec_())