from PyQt6.QtWidgets import QDialog, QLineEdit, QLabel, QPushButton, QGridLayout, QHBoxLayout, QMessageBox, QCheckBox
from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt


class PSDInputDialog(QDialog):
    """添加密码对话框
    """
    def __init__(self):
        super().__init__()
        self.initUI()
        
        self.setMinimumSize(400, 360)
        self.setMaximumSize(400, 360)

    def initUI(self):
        self.setWindowTitle("添加密码")
        
        # 用户信息输入
        self.websiteEdit = QLineEdit(self)
        self.usernameEdit = QLineEdit(self)
        self.psdEdit = QLineEdit(self)
        
        self.psdEdit.returnPressed.connect(self.onOkClicked)
        self.psdEdit.setEchoMode(QLineEdit.EchoMode.Password) # 不可见
        
        
        # 标签
        website_lbl = QLabel("网站：")
        name_lbl = QLabel("账号：")
        psd_lbl = QLabel("密码：")

        # 显示、隐藏密码
        check = QCheckBox("显示密码")
        check.toggle()
        check.setCheckState(Qt.CheckState.Unchecked)
        check.stateChanged.connect(self.change)

        # 提交按钮
        btn = QPushButton('OK', self)
        btn.clicked.connect(self.onOkClicked)
        
        # 设置文字样式
        font = QFont()
        font.setPixelSize(16)
        
        self.websiteEdit.setFont(font)
        self.usernameEdit.setFont(font)
        self.psdEdit.setFont(font)
        
        website_lbl.setFont(font)
        name_lbl.setFont(font)
        psd_lbl.setFont(font)

        btn.setFont(font)    
            
        # 提交按钮水平居中
        hbox = QHBoxLayout()
        hbox.addStretch(1)
        hbox.addWidget(btn)
        hbox.addStretch(1)
        
        # 表格排列
        grid = QGridLayout()
        grid.addWidget(website_lbl, 0, 0)
        grid.addWidget(self.websiteEdit, 0, 1)
        grid.addWidget(name_lbl, 1, 0)
        grid.addWidget(self.usernameEdit, 1, 1)
        grid.addWidget(psd_lbl, 2, 0)
        grid.addWidget(self.psdEdit, 2, 1)
        grid.addWidget(check, 3, 0, 1, 2)
        grid.addLayout(hbox, 4, 0, 1, 2)

        
        self.setLayout(grid)
       
    def onOkClicked(self):
        website = self.websiteEdit.text()
        account = self.usernameEdit.text()
        password = self.psdEdit.text()
        
        if website.strip() == "":  # 检查 websiteEdit 是否为空（或只包含空白字符）
            QMessageBox.warning(self, "提示", "请输入网站")
            return
        if account.strip() == "":
            QMessageBox.warning(self, "提示", "请输入用户名")
            return
        if password.strip() == "":
            QMessageBox.warning(self, "提示", "请输入密码")
            return
        
        self.accept()  # 如果 QLineEdit 中有文本，则接受对话框（关闭并返回 QDialog.Accepted）
     
    def change(self, state):
        if state == Qt.CheckState.Checked.value:
            self.psdEdit.setEchoMode(QLineEdit.EchoMode.Normal)
        
        else:
            self.psdEdit.setEchoMode(QLineEdit.EchoMode.Password)