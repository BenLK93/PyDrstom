import sys
from timestamp_window_ui_class import *


def main():
    app = QApplication(sys.argv)  
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())
    app.setQuitOnLastWindowClosed(False)

main()