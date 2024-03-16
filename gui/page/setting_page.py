from PyQt6.QtWidgets import QWidget, QLabel, QVBoxLayout, QListWidget, QListWidgetItem, QMessageBox
from gui.dialog.user_psd_change_dialog import UserPSDChangeDialog
from manage.users import UsersManage
from PyQt6.QtGui import QIcon, QFont
from PyQt6.QtCore import QSize
from logger.log import log

class SettingPage(QWidget):
    
    def __init__(self):
        super().__init__()
        self.user_manage = UsersManage()
        self.initUI()
        
    def initUI(self):
        self.layout = QVBoxLayout(self)
        
        self.list_widget = QListWidget(self)
        
        self.layout.addWidget(self.list_widget)
        
        self.add_list_widget("修改密码", r".\assets\icon\psd_change.png")
        
        

        self.list_widget.itemClicked.connect(self.itemClicked)

    
    def add_list_widget(self, title: str, icon: str):
        font = QFont()
        font.setPixelSize(20)
        
        item = QListWidgetItem(self.list_widget)
        item.setSizeHint(QSize(100, 50))
        item.setIcon(QIcon(icon))
        
        label = QLabel(title, self)
        label.setFont(font)
        self.list_widget.setItemWidget(item, label)
    

    def itemClicked(self, item):
        setting = self.list_widget.itemWidget(item).text()
        if setting == "修改密码":
            self.user_psd_change()
            
            
    def user_psd_change(self):
        user_psd_change_dialog = UserPSDChangeDialog()
        
        if user_psd_change_dialog.exec():
            user = self.user_manage.get_login()
            old_psd = user_psd_change_dialog.old_psdEdit.text()
            new_psd = user_psd_change_dialog.new_psdEdit.text()
            
            if self.user_manage.change_psd(user, old_psd, new_psd):
                log.info("修改用户密码成功")
                QMessageBox.information(self, "修改密码", "修改密码成功")
            else:
                log.info("修改密码失败")
                QMessageBox.information(self, "修改密码", "修改密码失败")
            
