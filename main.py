import sys
from PyQt6.QtWidgets import QApplication
from gui.main import MainWindow
from logger.log import log


def main():
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    main_window = MainWindow()
    sys.exit(app.exec())


if __name__ == "__main__":
    log.info("程序开始运行...")
    main()
    log.info("程序结束运行")