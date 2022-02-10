import sys
import requests
from PyQt5 import uic
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtCore import Qt, QCoreApplication
from IPython.external.qt_for_kernel import QtCore


class MyWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('untitled.ui', self)
        self.z = 3
        self.pixmap = QPixmap()
        self.initUI()

    def initUI(self):
        self.pushButton.clicked.connect(self.update)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_PageUp:
            self.z += 1
            self.update()

        if event.key() == Qt.Key_PageDown:
            self.z -= 1
            self.update()

        if event.key() == Qt.Key_Escape:
            QCoreApplication.instance().quit()

    def update(self):
        api_server = "http://static-maps.yandex.ru/1.x/"
        lon = self.line_latitude.text()
        lat = self.line_altitude.text()
        params = {
            "ll": ",".join([lon, lat]),
            "z": self.z % 18,
            "l": "map"
        }
        response = requests.get(api_server, params=params)
        if not response:
            print("Ошибка выполнения запроса:")
            print("Http статус:", response.status_code, "(", response.reason, ")")
            sys.exit(1)
        payload = QtCore.QByteArray(response.content)
        self.pixmap.loadFromData(payload, "png")
        self.image.setPixmap(self.pixmap)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyWidget()
    ex.show()
    sys.exit(app.exec())
