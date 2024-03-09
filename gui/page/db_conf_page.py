from PyQt6.QtWidgets import QPushButton, QWidget, QLabel, QVBoxLayout, QHBoxLayout, QGridLayout, QLineEdit, QMessageBox
from manage.manage_psd import manage

class DBConfPage(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        
    def initUI(self):
        self.db_conf = QWidget()
        self.create_db_conf_widget()
        
        hbox = QHBoxLayout()
        hbox.addStretch(1)
        hbox.addWidget(self.db_conf)
        hbox.addStretch(1)
        
        vbox = QVBoxLayout()
        vbox.addStretch(1)
        vbox.addLayout(hbox)
        vbox.addStretch(1)
        
        self.setLayout(vbox)
    
    def create_db_conf_widget(self):
        host = QLabel("主机：")
        user = QLabel("账号：")
        password = QLabel("密码：")
        
        db_conf = manage.get_db_conf()
        
        self.hostEdit = QLineEdit(db_conf["host"], self)
        self.userEdit = QLineEdit(db_conf["user"], self)
        self.passwordEdit = QLineEdit("********", self)
        self.passwordEdit.setEchoMode(QLineEdit.EchoMode.Password)
        
        self.btn = QPushButton("OK", self)
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
        
        
    def update_db_conf(self):
        host = self.hostEdit.text()
        user = self.userEdit.text()
        password = self.passwordEdit.text()
        
        if host.strip() == "":  # 检查 websiteEdit 是否为空（或只包含空白字符）
            QMessageBox.warning(self, "提示", "请输入主机地址")
            return
        if user.strip() == "":
            QMessageBox.warning(self, "提示", "请输入用户名")
            return
        if password.strip() == "":
            QMessageBox.warning(self, "提示", "请输入密码")
            return
        
        manage.create_db_config(host, user, password)
        manage.update_db_manage()
        
        
        