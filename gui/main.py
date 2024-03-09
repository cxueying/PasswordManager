from PyQt6.QtWidgets import QWidget, QHBoxLayout, QMainWindow, QStatusBar
from gui.menu import MainMenu
from gui.container import MainContainer


class MainWindow(QMainWindow):
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("密码管理器")
        self.setMinimumSize(640, 360)
        self.resize(1280, 720)
        # 居中显示
        self.frameGeometry().moveCenter(self.screen().availableGeometry().center())
        self.initUI()
        self.show()
        
        
    def initUI(self):
        self.container = MainContainer(self)  # 创建主界面容器
        self.menu = MainMenu(self, self.container)  # 创建菜单栏
        
        self.statusBar = QStatusBar(self)
        self.setStatusBar(self.statusBar)

        self.menu.setFixedWidth(150)  # 设置菜单栏的固定宽度

        # 使用水平布局将菜单和主界面并排放置
        self.centralWidget = QWidget(self)
        self.setCentralWidget(self.centralWidget)
        layout = QHBoxLayout(self.centralWidget)
        layout.addWidget(self.menu)
        layout.addWidget(self.container)
        
        
        
        