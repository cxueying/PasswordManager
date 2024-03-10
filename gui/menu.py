from PyQt6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QApplication
from PyQt6.QtGui import QFont
from gui.container import MainContainer


class MenuButton(QPushButton):
    def __init__(self, text):
        super().__init__(text)
        self.setMinimumSize(130, 50)


class MainMenu(QWidget):
    def __init__(self, parent, container: MainContainer):
        super().__init__(parent)
        self.container = container
        self.initUI()
        
    def initUI(self):
        self.layout = QVBoxLayout(self) # 使用垂直布局
        
        main_button = MenuButton("主界面")
        main_button.clicked.connect(lambda: self.container.setCurrentIndex(0))
        self.layout.addWidget(main_button)
        
        db_conf_button = MenuButton("数据库配置")
        db_conf_button.clicked.connect(lambda: self.container.setCurrentIndex(1))
        self.layout.addWidget(db_conf_button)
        
        self.layout.addStretch()
        
        exit_button = MenuButton("退出")
        exit_button.clicked.connect(QApplication.instance().quit)
        self.layout.addWidget(exit_button)


