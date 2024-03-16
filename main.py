from gui.db_conf import DBConfPage
import sys
from PyQt6.QtWidgets import QApplication
from logger.log import log


def main():
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    db_conf_page = DBConfPage()
    sys.exit(app.exec())


if __name__ == "__main__":
    log.info("程序开始运行...")
    main()