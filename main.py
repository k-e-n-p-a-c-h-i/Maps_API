import sys
import requests
from PyQt5 import uic
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtCore import Qt, QCoreApplication


class MyWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        self.img = QImage()
        uic.loadUi('untitled.ui', self)
        self.z = 8
        self.layer = 'map'
        self.pixmap = QPixmap()
        self.initUI()

    def initUI(self):
        self.pushButton.clicked.connect(self.update)
        self.comboBox.addItems(['схема', 'спутник', 'гибрид'])
        self.setFixedSize(601, 619)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_PageUp:
            if self.z < 17:
                self.z += 1
            self.update()

        if event.key() == Qt.Key_PageDown:
            if self.z > 0:
                self.z -= 1
            self.update()

        if event.key() == Qt.Key_Escape:
            QCoreApplication.instance().quit()

    def update(self):
        api_server = "http://static-maps.yandex.ru/1.x/"
        lon = self.line_latitude.text()
        lat = self.line_altitude.text()
        selected_layer = self.comboBox.currentText()

        if selected_layer == 'схема':
            self.layer = 'map'

        if selected_layer == 'спутник':
            self.layer = 'sat'

        if selected_layer == 'гибрид':
            self.layer = 'sat,skl'

        params = {
            "ll": ",".join([lon, lat]),
            "z": self.z,
            "l": self.layer
        }
        response = requests.get(api_server, params=params, stream=True)
        self.img.loadFromData(response.content)
        self.image.setPixmap(QPixmap.fromImage(self.img))

        if not response:
            print("Ошибка выполнения запроса:")
            print("Http статус:", response.status_code, "(", response.reason, ")")
            sys.exit(1)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyWidget()
    ex.show()
    sys.exit(app.exec())
