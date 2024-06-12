import sys
from PyQt5.QtWidgets import QApplication
from ultimate_tic_tac_toe import UltimateTicTacToe

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = UltimateTicTacToe()
    window.show()
    sys.exit(app.exec_())
