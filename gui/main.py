from PyQt6.QtWidgets import QWidget, QHBoxLayout, QMainWindow, QStatusBar, QVBoxLayout, QPushButton, QStackedWidget, QApplication
from PyQt6.QtGui import QIcon
from PyQt6.QtCore import QSize
from gui.page.psd_manage_page import PSDManagePage
from gui.page.setting_page import SettingPage


class MainWindow(QMainWindow):
    
    class MenuButton(QPushButton):
        def __init__(self, text):
            super().__init__(text)
            self.setMinimumSize(150, 50)
    
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
        self.menu = QWidget(self)   # 主菜单
        self.main_container = QStackedWidget(self)     # 主界面
        
        self.main_container_init()
        self.menu_init()
        
        # 状态栏
        self.statusBar = QStatusBar(self)
        self.setStatusBar(self.statusBar)
        
        
        # 使用水平布局将菜单和主界面并排放置
        self.centralWidget = QWidget(self)
        self.setCentralWidget(self.centralWidget)
        layout = QHBoxLayout(self.centralWidget)
        layout.addWidget(self.menu)
        layout.addWidget(self.main_container)


    def main_container_init(self):
        # 创建页面
        self.psd_manage_page = PSDManagePage(self)
        self.setting_page = SettingPage()
        
        
        # 添加页面
        self.main_container.addWidget(self.psd_manage_page)
        self.main_container.addWidget(self.setting_page)
        
        
    def menu_init(self):
        vbox = QVBoxLayout()

        main_button = self.MenuButton("密码管理")
        main_button.setIcon(QIcon(r".\assets\icon\password.png"))
        main_button.setIconSize(QSize(32, 32))
        main_button.clicked.connect(self.toggle_psd_manage_page)
    
        setting_button = self.MenuButton("设置")
        setting_button.setIcon(QIcon(r".\assets\icon\setting.png"))
        setting_button.setIconSize(QSize(32, 32))
        setting_button.clicked.connect(lambda: self.main_container.setCurrentIndex(1))
            
        exit_button = self.MenuButton("退出")
        exit_button.setIcon(QIcon(r".\assets\icon\close.png"))
        exit_button.setIconSize(QSize(32, 32))
        exit_button.clicked.connect(QApplication.instance().quit)
        
        vbox.addWidget(main_button)
        
        # 放置到底部
        vbox.addStretch()
        vbox.addWidget(setting_button)
        vbox.addWidget(exit_button)
        
        self.menu.setLayout(vbox)
        
    
    def toggle_psd_manage_page(self):
        self.psd_manage_page.fresh_psd_table()
        self.main_container.setCurrentIndex(0)


    def showEvent(self, event):
        super().showEvent(event)
        # 设置焦点
        self.menu.setFocus()