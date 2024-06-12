from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QFrame, QLineEdit, QPushButton, QFileDialog, QColorDialog
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt

class PlayerDisplay(QWidget):
    def __init__(self, player_image, player_name='Игрок'):
        super().__init__()
        self.layout = QVBoxLayout(self)

        self.label = QLabel(self)
        self.setImage(player_image)
        self.layout.addWidget(self.label, alignment=Qt.AlignHCenter)

        self.indicator = QFrame(self)
        self.indicator.setFrameShape(QFrame.HLine)
        self.indicator.setFrameShadow(QFrame.Sunken)
        self.default_color = "#344C11"
        self.indicator.setStyleSheet(f"background-color: {self.default_color}")
        self.indicator.setFixedHeight(4)
        self.layout.addWidget(self.indicator, alignment=Qt.AlignHCenter)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.addSpacing(5)

        self.indicator.setVisible(False)

        self.nameLineEdit = QLineEdit(self)
        self.nameLineEdit.setText(player_name)
        self.nameLineEdit.textChanged.connect(self.updateName)
        self.layout.addWidget(self.nameLineEdit, alignment=Qt.AlignHCenter)
        self.layout.addSpacing(5)

        self.uploadButton = QPushButton("Загрузить фото", self)
        self.uploadButton.clicked.connect(self.uploadImage)
        self.layout.addWidget(self.uploadButton, alignment=Qt.AlignHCenter)
        self.layout.addSpacing(5)

        self.colorButton = QPushButton("Выбрать цвет", self)
        self.colorButton.clicked.connect(self.selectColor)
        self.layout.addWidget(self.colorButton, alignment=Qt.AlignHCenter)
        self.layout.addSpacing(5)

    def setImage(self, image_path):
        self.label.setPixmap(QPixmap(image_path).scaled(100, 100, Qt.KeepAspectRatio))

    def updateName(self):
        self.nameLineEdit.setText(self.nameLineEdit.text().strip())

    def setActive(self, active):
        self.indicator.setVisible(active)

    def uploadImage(self):
        file_name, _ = QFileDialog.getOpenFileName(self, "Открыть", "", "Картинки (*.png *.jpg *.bmp)")
        if file_name:
            self.setImage(file_name)

    def selectColor(self):
        color = QColorDialog.getColor()
        if color.isValid():
            self.indicator.setStyleSheet(f"background-color: {color.name()}")
            self.default_color = color.name()
