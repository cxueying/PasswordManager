from PyQt6.QtWidgets import QWidget, QLabel, QVBoxLayout, QListWidget, QListWidgetItem, QMessageBox, QPushButton, QHBoxLayout
from gui.dialog.user_psd_change_dialog import UserPSDChangeDialog
from manage.users import UsersManage
from PyQt6.QtGui import QIcon, QFont, QDesktopServices
from PyQt6.QtCore import QSize, Qt, QUrl
from logger.log import log

class SettingPage(QWidget):
    
    class SettingMenu(QPushButton):
        
        def __init__(self, title, icon):
            super().__init__(QIcon(icon), title)
            self.initUI()
        
        def initUI(self):
            font = QFont()
            font.setPixelSize(20)
            self.setFont(font)
            self.setIconSize(QSize(32, 32))
            self.setFixedHeight(50)
            self.setFixedWidth(self.size().width()  )
            self.setStyleSheet("border: none; text-align: left;")
        
        def setConnet(self, func):
            self.clicked.connect(lambda: func())
    
    def __init__(self):
        super().__init__()
        self.user_manage = UsersManage()
        self.initUI()
        
    def initUI(self):
        self.setting_widget = QWidget(self)
        
        self.psd_change_menu = self.SettingMenu("修改密码", r".\assets\icon\psd_change.png")
        self.psd_change_menu.setConnet(self.user_psd_change)
        
        self.about_menu = self.SettingMenu("关于", r".\assets\icon\about.png")
        self.about_menu.setConnet(self.about)
        
        
        vbox = QVBoxLayout(self)
        vbox.addWidget(self.psd_change_menu)
        vbox.addWidget(self.about_menu)
        vbox.addStretch(1)
        
        self.setting_widget.setLayout(vbox)
            
            
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
            

    def about(self):
        self.setting_widget.close()
        
        font = QFont()
        font.setPixelSize(20)
        
        about_widget = QWidget(self)
        about_widget.resize(self.size())
        
        def test():
            about_widget.close()
            self.setting_widget.show()
            
        return_button = self.SettingMenu("返回", r".\assets\icon\left_1.png")
        return_button.setConnet(test)
        
        
        about_txt = "版本号：v2.3.3\n开发者：Eroz"
        
        about_lbl = QLabel()
        about_lbl.setText(about_txt)
        about_lbl.setFont(font)
        about_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter) # 居中对齐
        
        def open_link():
            QDesktopServices.openUrl(QUrl("https://github.com/cxueying"))
        github_lbl = QLabel("<a href='#'>GitHub</a>")
        github_lbl.linkActivated.connect(open_link)
        github_lbl.setFont(font)
        github_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)

        vbox = QVBoxLayout()
        vbox.addWidget(return_button)
        vbox.addStretch(1)
        vbox.addWidget(about_lbl)
        vbox.addWidget(github_lbl)
        
        about_widget.setLayout(vbox)
        about_widget.show()