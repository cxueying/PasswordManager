from PyQt6.QtWidgets import QWidget,QStackedWidget, QMainWindow
from gui.page.psd_manage_page import PSDManagePage
from gui.page.db_conf_page import DBConfPage


class MainContainer(QWidget):
    def __init__(self, parent: QMainWindow):
        self.parent = parent
        super().__init__()
        self.initUI()
        
    def initUI(self):
        self.container = QStackedWidget(self)
        
        self.psd_manage_page = PSDManagePage(self.parent)
        db_conf_page = DBConfPage()
        
        # 添加页面
        self.container.addWidget(self.psd_manage_page)
        self.container.addWidget(db_conf_page)
        
        
    def setCurrentIndex(self, page_num):
        if page_num == 0:
            self.psd_manage_page.fresh_psd_table()
        self.container.setCurrentIndex(page_num)
    
    
    # 随着窗口大小改变改变 container 的大小
    def resizeEvent(self, e):
        self.container.setGeometry(
            0,
            0,
            self.parent.size().width() - 180,
            self.parent.size().height() - 30
        )
        
    
