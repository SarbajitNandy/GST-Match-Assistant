from src.main.frontend.automatch import Ui_MainWindow
from PyQt5 import QtWidgets

import sys

if __name__ == "__main__":
    # logging.basicConfig(filename="assets/log/AutoMatch_Log.txt", level=logging.INFO, format="%(asctime)s : %(levelname)s : %(lineno)d : %(message)s")

    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())