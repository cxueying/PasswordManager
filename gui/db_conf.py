from PyQt6.QtWidgets import QLineEdit, QLabel, QPushButton, QGridLayout, QHBoxLayout, QWidget, QMessageBox
from PyQt6.QtGui import QFont
from gui.login import Login
from DB.init import db_init
from logger.log import log

class DBConfPage(QWidget):
    """配置数据库连接对话框
    """
    def __init__(self):
        super().__init__()
        
        if self.__check_connected() == True:
            # 数据库连接成功，转到 Login 界面
            
            # 若不将 login 实例保存为DBConfPage 的一个属性，则在 __init__ 结束后会被销毁， 界面一闪而过
            self.login = Login()
            
        else:
            log.info("数据库连接失败，创建数据库连接界面")
            
            self.setWindowTitle("连接数据库")
            self.setMinimumSize(400, 360)
            self.setMaximumSize(400, 360)
            # 居中显示
            self.frameGeometry().moveCenter(self.screen().availableGeometry().center())
            self.initUI()
            self.show()


    def __check_connected(self):
        if db_init.get_conn() != None:
            return True
        else:
            return False
            

    def initUI(self):
        font = QFont()
        font.setPixelSize(16)
        
        # 用户信息输入
        self.hostEdit = QLineEdit(self)
        self.userEdit = QLineEdit(self)
        self.psdEdit = QLineEdit(self)
        self.psdEdit.setEchoMode(QLineEdit.EchoMode.Password) # 不可见
        
        # 标签
        host_lbl = QLabel("主机：")
        user_lbl = QLabel("用户：")
        psd_lbl = QLabel("密码：")

        # 提交按钮
        btn = QPushButton('OK', self)
        btn.setDefault(True)
        btn.clicked.connect(self.create_conn)
        
        # 设置字体样式
        self.hostEdit.setFont(font)
        self.userEdit.setFont(font)
        self.psdEdit.setFont(font)
        
        host_lbl.setFont(font)
        user_lbl.setFont(font)
        psd_lbl.setFont(font)
        
        btn.setFont(font)
        
        # 提交按钮水平居中
        hbox = QHBoxLayout()
        hbox.addStretch(1)
        hbox.addWidget(btn)
        hbox.addStretch(1)
        
        # 表格排列
        grid = QGridLayout()
        grid.addWidget(host_lbl, 0, 0)
        grid.addWidget(self.hostEdit, 0, 1)
        grid.addWidget(user_lbl, 1, 0)
        grid.addWidget(self.userEdit, 1, 1)
        grid.addWidget(psd_lbl, 2, 0)
        grid.addWidget(self.psdEdit, 2, 1)
        grid.addLayout(hbox, 3, 0, 1, 2)   
        
        self.setLayout(grid)
        

    def create_conn(self):
        host = self.hostEdit.text()
        user =self.userEdit.text()
        password = self.psdEdit.text()
        
        if host.strip() == "":  # 检查 websiteEdit 是否为空（或只包含空白字符）
            QMessageBox.warning(self, "提示", "请输入网站")
            return
        if user.strip() == "":
            QMessageBox.warning(self, "提示", "请输入用户名")
            return
        if password.strip() == "":
            QMessageBox.warning(self, "提示", "请输入密码")
            return

        db_init.create_config(host, user, password)
        db_init.re_conn()
        
        if db_init.get_conn() == None:
            QMessageBox.warning(self, "提示", "数据库连接失败")
            return
        
        else:
            self.close()
            self.login = Login()
        
        
        