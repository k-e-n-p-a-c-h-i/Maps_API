import sys

from PyQt5 import uic
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QMessageBox
from PyQt5.QtCore import Qt, QCoreApplication
from IPython.external.qt_for_kernel import QtCore

import requests


class BadRequest(Exception):
    pass


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
        try:
            map_request = f"https://static-maps.yandex.ru/1.x/?ll={self.lineEdit_2.text()},{self.lineEdit.text()}&l=map&z={self.spinBox.value()}"
            response = requests.get(map_request)
            if not response:
                raise BadRequest
            payload = QtCore.QByteArray(response.content)
            self.pixmap = QPixmap()
            self.pixmap.loadFromData(payload, "png")
            self.image.setPixmap(self.pixmap)
        except BadRequest:
            QMessageBox.critical(self, "Ошибка", "Недопустимый формат данных", QMessageBox.Ok)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyWidget()
    ex.show()
    sys.exit(app.exec())