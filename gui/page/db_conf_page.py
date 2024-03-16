from PyQt6.QtWidgets import QPushButton, QWidget, QLabel, QVBoxLayout, QHBoxLayout, QGridLayout, QLineEdit, QMessageBox
from PyQt6.QtGui import QFont

class DBConfPage(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        
    def initUI(self):
        self.db_conf = QWidget()
        self.create_db_conf_widget()
        
        self.db_info = QWidget()
        self.create_db_info_widget()
        
        hbox = QHBoxLayout()
        hbox.addStretch(1)
        hbox.addWidget(self.db_conf)
        hbox.addStretch(1)
        
        vbox = QVBoxLayout()
        vbox.addWidget(self.db_info)
        vbox.addStretch(1)
        vbox.addLayout(hbox)
        vbox.addStretch(1)
        
        self.setLayout(vbox)
    
    def create_db_conf_widget(self):
        host = QLabel("主机：")
        user = QLabel("账号：")
        password = QLabel("密码：")
        
        # 设置字体大小
        font = QFont()
        font.setPointSize(16)
        
        host.setFont(font)
        user.setFont(font)
        password.setFont(font)
        
        db_conf = None
        
        if db_conf == None:
            self.hostEdit = QLineEdit(self)
            self.userEdit = QLineEdit(self)
            self.passwordEdit = QLineEdit(self)
            self.passwordEdit.setEchoMode(QLineEdit.EchoMode.Password)
        else:
            self.hostEdit = QLineEdit(db_conf["host"], self)
            self.userEdit = QLineEdit(db_conf["user"], self)
            self.passwordEdit = QLineEdit("********", self)
            self.passwordEdit.setEchoMode(QLineEdit.EchoMode.Password)
        
        self.hostEdit.setFont(font)
        self.userEdit.setFont(font)
        self.passwordEdit.setFont(font)
        
        self.btn = QPushButton("OK", self)
        self.setFont(font)
        hbox = QHBoxLayout()
        hbox.addStretch(1)
        hbox.addWidget(self.btn)
        hbox.addStretch(1)
        self.btn.clicked.connect(self.update_db_conf)
        
        grib = QGridLayout()
        grib.addWidget(host, 0, 0)
        grib.addWidget(self.hostEdit, 0, 1)
        grib.addWidget(user, 1, 0)
        grib.addWidget(self.userEdit, 1, 1)
        grib.addWidget(password, 2, 0)
        grib.addWidget(self.passwordEdit, 2, 1)
        
        vbox = QVBoxLayout()
        vbox.addLayout(grib)
        vbox.addLayout(hbox)
        
        self.db_conf.setLayout(vbox)
        
        
    # def update_db_conf(self):
    #     host = self.hostEdit.text()
    #     user = self.userEdit.text()
    #     password = self.passwordEdit.text()
        
    #     if host.strip() == "":  # 检查 websiteEdit 是否为空（或只包含空白字符）
    #         QMessageBox.warning(self, "提示", "请输入主机地址")
    #         return
    #     if user.strip() == "":
    #         QMessageBox.warning(self, "提示", "请输入用户名")
    #         return
    #     if password.strip() == "":
    #         QMessageBox.warning(self, "提示", "请输入密码")
    #         return
        
    #     manageInit.create_config(host, user, password)
    #     manageInit.update_db_init()
    #     self.set_db_status_style()
        
        
    def create_db_info_widget(self):
        db_status_title = QLabel("数据库状态：")
        self.db_status = QLabel()
        
        font = QFont()
        font.setPointSize(16)
        
        db_status_title.setFont(font)
        self.db_status.setFont(font)
        
        self.set_db_status_style()
        
        hbox = QHBoxLayout()
        hbox.addWidget(db_status_title)
        hbox.addWidget(self.db_status)
        hbox.addStretch(1)
        
        
        self.db_info.setLayout(hbox)
        
    # def set_db_status_style(self):
    #     if manageInit.connected:
    #         self.db_status.setText("已连接")
    #         self.db_status.setStyleSheet("""
    #             QLabel {
    #                 color: #00FF00;
    #             }
    #         """)
        
    #     else:
    #         self.db_status.setText("未连接")
    #         self.db_status.setStyleSheet("""
    #             QLabel {
    #                 color: #FF0000;
    #             }
    #         """)