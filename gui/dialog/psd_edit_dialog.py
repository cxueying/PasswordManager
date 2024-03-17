from PyQt6.QtWidgets import QDialog, QGridLayout, QLabel, QLineEdit, QPushButton, QMessageBox, QHBoxLayout, QCheckBox
from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt

class PSDEditDialog(QDialog):
    
    def __init__(self, **kwargs):
        super().__init__()
        self.psd_dict = kwargs
        self.initUI()
        
        self.setWindowTitle("编辑")
        self.setMaximumSize(400, 360)
        self.setMinimumSize(400, 360)
        
    def initUI(self):
        
        # 标签
        website = QLabel("网站：")
        account = QLabel("账号：")
        password = QLabel("密码：")
        
        # 编辑框
        self.websiteEdit = QLineEdit(self.psd_dict["website"], self)
        self.accountEdit = QLineEdit(self.psd_dict["account"], self)
        self.psdEdit = QLineEdit(self.psd_dict["password"], self)
        self.psdEdit.setEchoMode(QLineEdit.EchoMode.Password)
        
        # 显示、隐藏密码
        check = QCheckBox("显示密码")
        check.toggle()
        check.setCheckState(Qt.CheckState.Unchecked)
        check.stateChanged.connect(self.change)
        
        # 提交按钮
        btn = QPushButton("提交", self)
        btn.clicked.connect(self.onOkClicked)
        
        # 设置字体样式
        font = QFont()
        font.setPixelSize(16)
        
        website.setFont(font)
        account.setFont(font)
        password.setFont(font)
        self.websiteEdit.setFont(font)
        self.accountEdit.setFont(font)
        self.psdEdit.setFont(font)
        btn.setFont(font)
        
        hbox = QHBoxLayout()
        hbox.addStretch(1)
        hbox.addWidget(btn)
        hbox.addStretch(1)
        
        grid = QGridLayout()
        grid.addWidget(website, 0, 0)
        grid.addWidget(self.websiteEdit, 0, 1)
        grid.addWidget(account, 1, 0)
        grid.addWidget(self.accountEdit, 1, 1)
        grid.addWidget(password, 2, 0)
        grid.addWidget(self.psdEdit, 2, 1)
        grid.addWidget(check, 3, 0, 1, 2)
        grid.addLayout(hbox, 4, 0, 1, 2)

        
        self.setLayout(grid)
        
    def onOkClicked(self):
        website = self.websiteEdit.text()
        account = self.accountEdit.text()
        password = self.psdEdit.text()
        
        if website.strip() == "":
            QMessageBox.warning(self, "提示", "网站不能为空")
            return
        if account.strip() == "":
            QMessageBox.warning(self, "提示", "账号不能为空")
            return
        if password.strip() == "":
            QMessageBox.warning(self, "提示", "密码不能为空")
            return
        
        self.accept()
        
    def change(self, state):
        if state == Qt.CheckState.Checked.value:
            self.psdEdit.setEchoMode(QLineEdit.EchoMode.Normal)
        
        else:
            self.psdEdit.setEchoMode(QLineEdit.EchoMode.Password)