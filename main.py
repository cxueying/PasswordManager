import sys
# from command.cmd import cmds
from PyQt6.QtWidgets import QApplication
from gui.main import MainWindow
from logger.log import log

# def main():
#     while True:
#         cmd = input("PSDManage> ")
#         if cmd in cmds and cmds[cmd]() == 'exit':
#             break
#         elif not cmd in cmds:
#             log.info("未知指令\n")

def main():
    app = QApplication(sys.argv)
    main_window = MainWindow()
    sys.exit(app.exec())


if __name__ == "__main__":
    log.info("程序开始运行...")
    main()
    log.info("程序结束运行")