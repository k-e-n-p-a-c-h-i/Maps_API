import sys

from PyQt5 import uic
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel
from PyQt5.QtCore import Qt, QCoreApplication
from IPython.external.qt_for_kernel import QtCore

import requests


class MyWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('untitled.ui', self)
        self.d = 0
        self.initUI()

    def initUI(self):
        self.pushButton.clicked.connect(self.update)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_PageUp:
            if self.d < 100:
                self.d += 20
            self.update(self.d)

        if event.key() == Qt.Key_PageDown:
            if self.d > 0:
                self.d -= 20
            self.update(self.d)

        if event.key() == Qt.Key_Escape:
            QCoreApplication.instance().quit()

    def update(self, delta=0):
        api_server = "http://static-maps.yandex.ru/1.x/"
        lon = self.line_latitude.text()
        lat = self.line_altitude.text()
        if delta == 0:
            delta = self.d
        delta = str((101 - delta) / 100)

        params = {
            "ll": ",".join([lon, lat]),
            "spn": ",".join([delta, delta]),
            "l": "map"
        }
        response = requests.get(api_server, params=params)
        if not response:
            print("Ошибка выполнения запроса:")
            print("Http статус:", response.status_code, "(", response.reason, ")")
            sys.exit(1)
        payload = QtCore.QByteArray(response.content)
        self.pixmap = QPixmap()
        self.pixmap.loadFromData(payload, "png")
        self.image.setPixmap(self.pixmap)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyWidget()
    ex.show()
    sys.exit(app.exec())