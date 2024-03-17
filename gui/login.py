from PyQt6.QtWidgets import QWidget, QPushButton, QGridLayout, QLabel, QLineEdit, QHBoxLayout, QMessageBox
from gui.main import MainWindow
from manage.users import UsersManage
from PyQt6.QtGui import QFont
from logger.log import log

class Login(QWidget):
    def __init__(self):
        super().__init__()
        self.user_manage = UsersManage()
        self.initUI()
        
        self.frameGeometry().moveCenter(self.screen().availableGeometry().center())
        self.setMinimumSize(400, 360)
        self.setMaximumSize(400, 360)
        self.setWindowTitle("登录")
        self.show()
        
    def initUI(self):
        user_label = QLabel("用户名：")
        psd_label = QLabel("密码：")
        
        # 显示登录用户
        user = self.user_manage.get_login()
        if user == None:
            self.userEdit = QLineEdit(self)
            self.psdEdit = QLineEdit(self)
            self.userEdit.setFocus()
        else:
            self.userEdit = QLineEdit(user, self)
            self.psdEdit = QLineEdit(self)
            self.psdEdit.setFocus()
        self.psdEdit.setEchoMode(QLineEdit.EchoMode.Password)
        self.psdEdit.returnPressed.connect(self.login)
         
        # 添加 登录 按钮
        btn = QPushButton("登录", self)
        btn.clicked.connect(self.login)
        # 取消默认选中状态
        btn.setAutoDefault(True)
        btn.setDefault(True)
        
        # 按钮水平居中
        hbox = QHBoxLayout()
        hbox.addStretch(1)
        hbox.addWidget(btn)
        hbox.addStretch(1)
        
        # 设置字体样式
        font = QFont()
        font.setPointSize(16)
        
        user_label.setFont(font)
        psd_label.setFont(font)
        self.userEdit.setFont(font)
        self.psdEdit.setFont(font)
        btn.setFont(font)
        
        # 布局全部元素
        grid = QGridLayout()
        grid.addWidget(user_label, 0, 0)
        grid.addWidget(self.userEdit, 0, 1)
        grid.addWidget(psd_label, 1, 0)
        grid.addWidget(self.psdEdit, 1, 1)
        grid.addLayout(hbox, 2, 0, 1, 2)
        
        self.setLayout(grid)
        
        
    def login(self):
        user = self.userEdit.text()
        psd = self.psdEdit.text()
        
        if user.strip() == "":
            QMessageBox.warning(self, "提示", "请输入账号")
            return
        if psd.strip() == "":
            QMessageBox.warning(self, "提示", "请输入密码")
            return

        if self.user_manage.login(user, psd):
            self.close()
            log.info("登录成功")
            self.user_manage.set_login(user)
            main_window = MainWindow()
        else:
            QMessageBox().warning(self, "提示", "账号或者密码错误")
            self.psdEdit.setText("")    # 清空输入的密码
            self.psdEdit.setFocus()     # 设置焦点
            return
            
        