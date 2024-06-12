from PyQt5.QtWidgets import QWidget, QGridLayout, QPushButton, QSizePolicy
from PyQt5.QtCore import Qt

class MiniBoard(QWidget):
    def __init__(self, mainGame, boardRow, boardCol):
        super().__init__()
        self.mainGame = mainGame
        self.boardRow = boardRow
        self.boardCol = boardCol
        self.layout = QGridLayout(self)
        self.buttons = [[QPushButton(self) for _ in range(3)] for _ in range(3)]

        for i in range(3):
            for j in range(3):
                self.layout.addWidget(self.buttons[i][j], i, j)
                self.buttons[i][j].setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
                self.buttons[i][j].setStyleSheet("color: #E8E1DB; font-size: 20px;")
                self.buttons[i][j].clicked.connect(lambda _, x=i, y=j: self.handleMove(x, y))

        self.winner = None

    def resizeEvent(self, event):
        super().resizeEvent(event)
        button_size = min(self.width() // 3, self.height() // 3)
        for row in self.buttons:
            for button in row:
                button.setFixedSize(button_size, button_size)

    def handleMove(self, x, y):
        if self.buttons[x][y].text() == '' and not self.winner:
            self.buttons[x][y].setText(self.mainGame.currentPlayer)
            self.checkMiniBoardWinner()
            self.mainGame.switchPlayer()
            if self.mainGame.miniBoards[x][y].winner is None:
                self.mainGame.setNextBoard(x, y)
            else:
                self.mainGame.setNextBoard(None, None)
            self.mainGame.checkWinner()

    def checkMiniBoardWinner(self):
        lines = [
            [self.buttons[i][0].text() for i in range(3)],
            [self.buttons[i][1].text() for i in range(3)],
            [self.buttons[i][2].text() for i in range(3)],
            [self.buttons[0][i].text() for i in range(3)],
            [self.buttons[1][i].text() for i in range(3)],
            [self.buttons[2][i].text() for i in range(3)],
            [self.buttons[i][i].text() for i in range(3)],
            [self.buttons[i][2 - i].text() for i in range(3)]
        ]

        for line in lines:
            if line[0] == line[1] == line[2] and line[0] != '':
                self.winner = line[0]
                self.setWinner(line[0])
                break

    def setWinner(self, winner):
        for row in self.buttons:
            for button in row:
                button.setText(winner)
                button.setEnabled(False)

    def resetBoard(self):
        for row in self.buttons:
            for button in row:
                button.setText('')
                button.setEnabled(True)
        self.winner = None
