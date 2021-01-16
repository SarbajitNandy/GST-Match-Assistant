from PyQt5.QtWidgets import QApplication

from src.main.frontend.domatch import do_match_gui

import sys


if __name__ == "__main__":
    app = QApplication(sys.argv)
    # Logging settings
    # logging.basicConfig(filename="assets/log/DoMatch_Log.txt", level=logging.INFO, format="%(asctime)s : %(levelname)s : %(lineno)d : %(message)s")

    main = do_match_gui()

    sys.exit(app.exec_())
