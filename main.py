import sys
from PyQt6.QtCore import Qt
from PyQt6 import QtCore, QtWidgets
from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget
import requests
from PyQt6.QtGui import QPixmap

MAP_FILE = "map.png"


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1064, 707)
        self.centralwidget = QtWidgets.QWidget(parent=MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.label_for_map = QtWidgets.QLabel(parent=self.centralwidget)
        self.label_for_map.setGeometry(QtCore.QRect(0, 0, 66, 18))
        self.label_for_map.setObjectName("label_for_map")
        self.search_line = QtWidgets.QLineEdit(parent=self.centralwidget)
        self.search_line.setGeometry(QtCore.QRect(940, 10, 113, 26))
        self.search_line.setText("")
        self.search_line.setObjectName("search_line")
        self.searchbutton = QtWidgets.QPushButton(parent=self.centralwidget)
        self.searchbutton.setGeometry(QtCore.QRect(950, 50, 88, 26))
        self.searchbutton.setObjectName("searchbutton")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(parent=MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1064, 23))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(parent=MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label_for_map.setText(_translate("MainWindow", "TextLabel"))
        self.searchbutton.setText(_translate("MainWindow", "Искать"))


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.z = 18
        self.z_dif = 1
        self.lat = 54.7224888
        self.lon = 30.457209
        self.theme = 'dark'
        self.change_coord = 0.0001 * self.z
        self.setup()

    def setup(self):
        self.label_for_map.setGeometry(0, 40, 800, 600)
        self.searchbutton.clicked.connect(
            lambda: self.find_place(self.search_line.text())
        )
        self.get_image()

    def get_image(self):
        api_key = 'f3a0fe3a-b07e-4840-a1da-06f18b2ddf13'
        params = {
            "ll": f"{self.lon},{self.lat}",
            "z": str(self.z),
            "apikey": api_key,
            "theme": self.theme
        }
        server_address = 'https://static-maps.yandex.ru/v1?'
        response = requests.get(server_address, params=params)

        with open('map.png', "wb") as file:
            file.write(response.content)

        pixmap = QPixmap('map.png')
        self.label_for_map.setPixmap(pixmap)
        self.label_for_map.resize(pixmap.width(), pixmap.height())

    def find_place(self, toponym_to_find):
        geocoder_api_server = "https://geocode-maps.yandex.ru/1.x/"
        geocoder_params = {
            "apikey": "8013b162-6b42-4997-9691-77b7074026e0",
            "geocode": toponym_to_find,
            "format": "json"
        }
        response = requests.get(geocoder_api_server, params=geocoder_params)
        json_response = response.json()
        toponym = json_response["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]
        lon, lat = toponym["Point"]["pos"].split()
        self.lon = float(lon)
        self.lat = float(lat)
        self.get_image()

    def keyPressEvent(self, event):
        step = 0.0005 * (21 - self.z + 1)

        if event.key() == Qt.Key.Key_PageUp and self.z < 21:
            self.z += self.z_dif
        elif event.key() == Qt.Key.Key_PageDown and self.z > 1:
            self.z -= self.z_dif
        elif event.key() == Qt.Key.Key_Left:
            self.lon -= step
        elif event.key() == Qt.Key.Key_Right:
            self.lon += step
        elif event.key() == Qt.Key.Key_Up:
            self.lat += step
        elif event.key() == Qt.Key.Key_Down:
            self.lat -= step
        elif event.key() == Qt.Key.Key_Space:
            if self.theme == "dark":
                self.theme = "light"
            elif self.theme == "light":
                self.theme = "dark"

        self.get_image()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
