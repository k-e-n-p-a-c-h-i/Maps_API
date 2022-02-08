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
        self.initUI()

    def initUI(self):
        self.pushButton.clicked.connect(self.update)


    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            QCoreApplication.instance().quit()

    def update(self):
        map_request = "https://static-maps.yandex.ru/1.x/?ll=134.619222%2C-26.400423&l=map&z=3"
        response = requests.get(map_request)
        if not response:
            print("Ошибка выполнения запроса:")
            print(map_request)
            print("Http статус:", response.status_code, "(", response.reason, ")")
            sys.exit(1)
        print('tyt')
        payload = QtCore.QByteArray(response.content)
        print(type(payload))
        self.pixmap = QPixmap()
        self.pixmap.loadFromData(payload, "png")
        self.image.setPixmap(self.pixmap)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyWidget()
    ex.show()
    sys.exit(app.exec())