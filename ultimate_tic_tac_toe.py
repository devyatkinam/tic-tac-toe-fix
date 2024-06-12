import json
import os
from PyQt5.QtWidgets import QMainWindow, QWidget, QHBoxLayout, QGridLayout, QMenuBar, QAction, QMessageBox, QColorDialog
from player_display import PlayerDisplay
from mini_board import MiniBoard

class UltimateTicTacToe(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Ultimate Tic Tac Toe')
        self.default_window_color = "#362E23"
        self.default_board_color = "#3A3C26"
        self.setStyleSheet(f"background-color: {self.default_window_color};")
        self.setFixedSize(1000, 800)

        self.initUI()

    def initUI(self):
        self.centralWidget = QWidget(self)
        self.centralWidget.setStyleSheet(f"background-color: {self.default_board_color};")
        self.setCentralWidget(self.centralWidget)
        self.mainLayout = QHBoxLayout(self.centralWidget)

        self.playerXDisplay = PlayerDisplay("default_x.png")
        self.playerODisplay = PlayerDisplay("default_o.png")

        self.mainLayout.addWidget(self.playerXDisplay)

        self.boardWidget = QWidget(self)
        self.boardLayout = QGridLayout(self.boardWidget)
        self.mainLayout.addWidget(self.boardWidget)

        self.miniBoards = [[MiniBoard(self, i, j) for j in range(3)] for i in range(3)]

        for i in range(3):
            for j in range(3):
                self.boardLayout.addWidget(self.miniBoards[i][j], i, j)

        self.mainLayout.addWidget(self.playerODisplay)

        self.currentPlayer = 'X'
        self.nextBoard = None
        self.updateBoardStates()
        self.updatePlayerIndicators()

        self.createMenu()

    def createMenu(self):
        menubar = QMenuBar(self)
        self.setMenuBar(menubar)

        gameMenu = menubar.addMenu("Игра")
        saveAction = QAction("Сохранить", self)
        saveAction.triggered.connect(self.saveGame)
        loadAction = QAction("Загрузить", self)
        loadAction.triggered.connect(self.loadGame)
        windowColorAction = QAction("Выбрать цвет окна", self)
        windowColorAction.triggered.connect(self.selectWindowColor)
        boardColorAction = QAction("Выбрать цвет поля", self)
        boardColorAction.triggered.connect(self.selectBoardColor)

        gameMenu.addAction(saveAction)
        gameMenu.addAction(loadAction)
        gameMenu.addAction(windowColorAction)
        gameMenu.addAction(boardColorAction)

    def switchPlayer(self):
        self.currentPlayer = 'O' if self.currentPlayer == 'X' else 'X'
        self.updatePlayerIndicators()

    def setNextBoard(self, i, j):
        if i is not None and j is not None and self.miniBoards[i][j].winner is None:
            self.nextBoard = (i, j)
        else:
            self.nextBoard = None
        self.updateBoardStates()

    def updateBoardStates(self):
        for i in range(3):
            for j in range(3):
                if self.nextBoard is None:
                    if self.miniBoards[i][j].winner is None:
                        self.miniBoards[i][j].setEnabled(True)
                        self.miniBoards[i][j].setStyleSheet("background-color: #A9AC5D;")
                    else:
                        self.miniBoards[i][j].setEnabled(False)
                        self.miniBoards[i][j].setStyleSheet("background-color: #6D6C3C;")
                else:
                    if (i, j) == self.nextBoard:
                        self.miniBoards[i][j].setEnabled(True)
                        self.miniBoards[i][j].setStyleSheet("background-color: #A9AC5D;")
                    else:
                        self.miniBoards[i][j].setEnabled(False)
                        self.miniBoards[i][j].setStyleSheet("background-color: #6D6C3C;")

    def updatePlayerIndicators(self):
        self.playerXDisplay.setActive(self.currentPlayer == 'X')
        self.playerODisplay.setActive(self.currentPlayer == 'O')

    def checkWinner(self):
        lines = [
            [(i, 0) for i in range(3)],
            [(i, 1) for i in range(3)],
            [(i, 2) for i in range(3)],
            [(0, i) for i in range(3)],
            [(1, i) for i in range(3)],
            [(2, i) for i in range(3)],
            [(i, i) for i in range(3)],
            [(i, 2 - i) for i in range(3)]
        ]

        for line in lines:
            symbols = [self.miniBoards[i][j].winner for i, j in line]
            if symbols[0] == symbols[1] == symbols[2] and symbols[0] is not None:
                winner_name = self.playerXDisplay.nameLineEdit.text() if symbols[0] == 'X' else self.playerODisplay.nameLineEdit.text()
                QMessageBox.information(self, 'Игра закончена!', f' {winner_name} выиграл(а)!')
                self.resetGame()
                return

    def resetGame(self):
        for row in self.miniBoards:
            for board in row:
                board.resetBoard()
        self.currentPlayer = 'X'
        self.nextBoard = None
        self.updateBoardStates()
        self.updatePlayerIndicators()

    def saveGame(self):
        game_state = {
            'currentPlayer': self.currentPlayer,
            'nextBoard': self.nextBoard,
            'boards': [
                [[cell.text() for cell in row] for row in board.buttons] for board_row in self.miniBoards for board in board_row
            ],
            'winners': [
                [board.winner for board in row] for row in self.miniBoards
            ],
            'windowColor': self.default_window_color,
            'boardColor': self.default_board_color
        }

        with open("save.txt", 'w') as file:
            json.dump(game_state, file)

    def loadGame(self):
        if not os.path.exists("save.txt"):
            QMessageBox.information(self, 'Load Game', 'Сохранения нет!')
            return

        with open("save.txt", 'r') as file:
            game_state = json.load(file)
            self.currentPlayer = game_state['currentPlayer']
            self.nextBoard = tuple(game_state['nextBoard']) if game_state['nextBoard'] else None

            for i, board_row in enumerate(self.miniBoards):
                for j, board in enumerate(board_row):
                    for x, row in enumerate(board.buttons):
                        for y, button in enumerate(row):
                            button.setText(game_state['boards'][i*3+j][x][y])
                            button.setEnabled(game_state['boards'][i*3+j][x][y] == '')

                    board.winner = game_state['winners'][i][j]

            self.default_window_color = game_state.get('windowColor', "#362E23")
            self.default_board_color = game_state.get('boardColor', "#3A3C26")
            self.setStyleSheet(f"background-color: {self.default_window_color};")
            self.centralWidget.setStyleSheet(f"background-color: {self.default_board_color};")
            self.updateBoardStates()
            self.updatePlayerIndicators()

    def selectWindowColor(self):
        color = QColorDialog.getColor()
        if color.isValid():
            self.default_window_color = color.name()
            self.setStyleSheet(f"background-color: {self.default_window_color};")

    def selectBoardColor(self):
        color = QColorDialog.getColor()
        if color.isValid():
            self.default_board_color = color.name()
            self.centralWidget.setStyleSheet(f"background-color: {self.default_board_color};")

if __name__ == '__main__':
    import sys
    from PyQt5.QtWidgets import QApplication

    app = QApplication(sys.argv)
    window = UltimateTicTacToe()
    window.show()
    sys.exit(app.exec_())
