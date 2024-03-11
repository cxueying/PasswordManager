from PyQt6.QtWidgets import QWidget, QPushButton, QGridLayout, QLabel, QLineEdit, QHBoxLayout, QMessageBox
from PyQt6.QtGui import QFont
from gui.main import MainWindow
from manage.manage_psd import manage
from logger.log import log

class Login(QWidget):
    def __init__(self):
        super().__init__()
        
        self.initUI()
        
    def initUI(self):
        user_label = QLabel("用户名：")
        psd_label = QLabel("密码：")
        
        user = manage.get_user_login()
        if user == None:
            self.userEdit = QLineEdit(self)
            self.psdEdit = QLineEdit(self)
            self.userEdit.setFocus()
        else:
            self.userEdit = QLineEdit(user, self)
            self.psdEdit = QLineEdit(self)
            self.psdEdit.setFocus()
        self.psdEdit.setEchoMode(QLineEdit.EchoMode.Password)
        
        btn = QPushButton("登录", self)
        btn.setDefault(True)
        btn.clicked.connect(self.login)
        
        hbox = QHBoxLayout()
        hbox.addStretch(1)
        hbox.addWidget(btn)
        hbox.addStretch(1)
        
        font = QFont()
        font.setPointSize(16)
        user_label.setFont(font)
        psd_label.setFont(font)
        self.userEdit.setFont(font)
        self.psdEdit.setFont(font)
        btn.setFont(font)
        
        grid = QGridLayout()
        grid.addWidget(user_label, 0, 0)
        grid.addWidget(self.userEdit, 0, 1)
        grid.addWidget(psd_label, 1, 0)
        grid.addWidget(self.psdEdit, 1, 1)
        grid.addLayout(hbox, 2, 0, 1, 2)
        
        self.setLayout(grid)
        
        self.frameGeometry().moveCenter(self.screen().availableGeometry().center())
        self.setMinimumSize(400, 300)
        self.setMaximumSize(400, 400)
        self.setWindowTitle("登录")
        self.show()
        
    def login(self):
        user = self.userEdit.text()
        psd = self.psdEdit.text()
        
        if user.strip() == "":
            QMessageBox.warning(self, "提示", "请输入账号")
            return
        if psd.strip() == "":
            QMessageBox.warning(self, "提示", "请输入密码")
            return
        
        if manage.login(user, psd):
            self.close()
            log.info("登录成功")
            manage.user_login(user)
            main_window = MainWindow()
        else:
            QMessageBox().warning(self, "提示", "账号或者密码错误")
            return
        
        