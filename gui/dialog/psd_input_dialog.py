from PyQt6.QtWidgets import QDialog, QLineEdit, QLabel, QPushButton, QGridLayout, QHBoxLayout, QWidget, QVBoxLayout, QMessageBox

class PSDInputDialog(QDialog):
    """添加密码对话框
    """
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("添加密码")
        
        # 用户信息输入
        self.websiteEdit = QLineEdit(self)
        self.usernameEdit = QLineEdit(self)
        self.psdEdit = QLineEdit(self)
        self.psdEdit.setEchoMode(QLineEdit.EchoMode.Password) # 不可见
        
        # 标签
        website_lbl = QLabel("网站：")
        name_lbl = QLabel("名字：")
        psd_lbl = QLabel("密码：")

        # 提交按钮
        self.btn = QPushButton('OK', self)
        self.btn.clicked.connect(self.onOkClicked)
        
        # 表格排列
        self.psd_input = QWidget()
        self.resize(300, 300)
        self.grid = QGridLayout()
        self.grid.addWidget(website_lbl, 0, 0)
        self.grid.addWidget(self.websiteEdit, 0, 1)
        self.grid.addWidget(name_lbl, 1, 0)
        self.grid.addWidget(self.usernameEdit, 1, 1)
        self.grid.addWidget(psd_lbl, 2, 0)
        self.grid.addWidget(self.psdEdit, 2, 1)
        self.psd_input.setLayout(self.grid)
        
        # 提交按钮水平居中
        self.hbox = QHBoxLayout()
        self.hbox.addStretch(1)
        self.hbox.addWidget(self.btn)
        self.hbox.addStretch(1)

        # 表格在上， 提交按钮在下
        self.vbox = QVBoxLayout()
        self.vbox.addWidget(self.psd_input)
        self.vbox.addLayout(self.hbox)
        
        
        self.setLayout(self.vbox)
       
    def onOkClicked(self):
        website = self.websiteEdit.text()
        account =self.usernameEdit.text()
        password = self.psdEdit.text()
        if website.strip() == "":  # 检查 websiteEdit 是否为空（或只包含空白字符）
            QMessageBox.warning(self, "提示", "请输入网站")
            return
        if account.strip() == "":
            QMessageBox.warning(self, "提示", "请输入用户名")
            return
        if password.strip() == "":
            QMessageBox.warning(self, "提示", "请输入密码")
            
        self.accept()  # 如果 QLineEdit 中有文本，则接受对话框（关闭并返回 QDialog.Accepted）
     
    def showEvent(self, event):
        super().showEvent(event)
        self.websiteEdit.setFocus()
        