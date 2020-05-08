import os
import sys

from PyQt5 import QtGui
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QFileDialog, QVBoxLayout, QLabel, QScrollArea
import numpy as np
import pydicom


class Dicom(QWidget):

    def __init__(self):
        super(Dicom, self).__init__()
        self.setWindowTitle('View Dicom Images')
        self.setGeometry(400, 200, 600, 600)
        button = QPushButton('Choose Directory Containing Dicom Files', self)
        button.setToolTip('Choose the folder containing dicom files')
        button.move(100, 70)
        button.clicked.connect(self.choose_directory)

        self.vbox = QVBoxLayout()
        self.vbox.addWidget(button)

        self.scrollArea = QScrollArea()
        self.vbox.addWidget(self.scrollArea)
        self.scrollArea.setWidgetResizable(True)
        self.scrollContent = QWidget(self.scrollArea)
        self.scrollLayout = QVBoxLayout(self.scrollContent)
        self.scrollContent.setLayout(self.scrollLayout)
        self.setLayout(self.vbox)

    def choose_directory(self):
        fname = QFileDialog.getExistingDirectory(self, "select directory")
        print(fname)
        self.convert_dicom(fname)

    def convert_dicom(self, file_path):
        for f in os.listdir(file_path):
            if f.endswith('.' + 'dcm'):
                l1 = QLabel()
                _data = pydicom.read_file(file_path + "\\" + f)
                print("Reading {file_path} +\\+ f}")

                raw_data = _data.RescaleSlope * _data.pixel_array + _data.RescaleIntercept
                data = (raw_data - (-1000)) / 4000 * 256
                data[data < 0] = 0
                data[data > 255] = 255
                data = data.astype("int8")
                _image = QtGui.QImage(data, data.shape[1], data.shape[0], QtGui.QImage.Format_Indexed8)
                pixmap = QtGui.QPixmap.fromImage(_image)
                l1.setPixmap(pixmap)
                self.scrollLayout.addWidget(l1)
        self.scrollArea.setWidget(self.scrollContent)


def main():
    app = QApplication(sys.argv)
    ex = Dicom()
    ex.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
