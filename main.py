import sys
import requests
from PyQt5 import uic
from PyQt5.QtGui import QPixmap, QImage, QMouseEvent
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtCore import Qt, QCoreApplication, QEvent


class MyWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        self.displacement_coefficient = {2: 8, 3: 7, 4: 6, 5: 4.5, 6: 1.2, 7: 1,
                                         8: 0.34, 9: 0.16, 10: 0.1, 11: 0.06,
                                         12: 0.01, 13: 0.01, 14: 0.008,
                                         15: 0.0038, 16: 0.002, 17: 0.000343}
        self.img = QImage()
        uic.loadUi('untitled.ui', self)
        self.z = 3
        self.layer = 'map'
        self.pixmap = QPixmap()
        self.initUI()

    def initUI(self):
        self.pushButton.clicked.connect(self.update)
        self.comboBox.addItems(['схема', 'спутник', 'гибрид'])
        self.setFixedSize(601, 619)
        self.image.installEventFilter(self)

    def eventFilter(self, obj, event):
        if obj == self.image:
            if event.type() == QEvent.MouseButtonPress:
                mouse_event = QMouseEvent(event)
                if mouse_event.buttons() == Qt.LeftButton:
                    self.setFocus()
        return QMainWindow.eventFilter(self, obj, event)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Up:
            if float(self.lineEdit_2.text()) + self.displacement_coefficient[self.z] <= 80:
                self.lineEdit_2.setText(str(float(self.lineEdit_2.text()) + self.displacement_coefficient[self.z]))
            self.update()

        if event.key() == Qt.Key_Down:
            if float(self.lineEdit_2.text()) - self.displacement_coefficient[self.z] >= -80:
                self.lineEdit_2.setText(str(float(self.lineEdit_2.text()) - self.displacement_coefficient[self.z]))
            self.update()

        if event.key() == Qt.Key_Left:
            if float(self.lineEdit.text()) - self.displacement_coefficient[self.z] >= -180:
                self.lineEdit.setText(str(float(self.lineEdit.text()) - self.displacement_coefficient[self.z]))
            self.update()

        if event.key() == Qt.Key_Right:
            if float(self.lineEdit.text()) + self.displacement_coefficient[self.z] <= 180:
                self.lineEdit.setText(str(float(self.lineEdit.text()) + self.displacement_coefficient[self.z]))
            self.update()

        if event.key() == Qt.Key_PageUp:
            if self.z < 17:
                self.z += 1
            self.update()

        if event.key() == Qt.Key_PageDown:
            if self.z > 2:
                self.z -= 1
            self.update()

        if event.key() == Qt.Key_Escape:
            QCoreApplication.instance().quit()

    def update(self):
        api_server = "http://static-maps.yandex.ru/1.x/"
        lon = self.lineEdit.text()
        lat = self.lineEdit_2.text()
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
