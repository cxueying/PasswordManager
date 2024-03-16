from PyQt6.QtWidgets import QDialog, QLineEdit, QLabel, QPushButton, QGridLayout, QHBoxLayout, QMessageBox
from PyQt6.QtGui import QFont
class UserPSDChangeDialog(QDialog):
    """修改用户密码对话框
    """
    def __init__(self):
        super().__init__()
        self.initUI()
        
        self.setMinimumSize(400, 360)
        self.setMaximumSize(400, 360)


    def initUI(self):
        self.setWindowTitle("修改密码")
        
        # 标签
        old_psd_lbl = QLabel("旧密码：")
        new_psd_lbl = QLabel("新密码：")
        new_psd_repeat_lbl = QLabel("重复新密码：")
        
        # 用户信息输入
        self.old_psdEdit = QLineEdit(self)
        self.new_psdEdit = QLineEdit(self)
        self.new_psd_repeatEdit = QLineEdit(self)
        
        self.old_psdEdit.setEchoMode(QLineEdit.EchoMode.Password) # 不可见
        self.new_psdEdit.setEchoMode(QLineEdit.EchoMode.Password)
        self.new_psd_repeatEdit.setEchoMode(QLineEdit.EchoMode.Password)
        
        self.new_psd_repeatEdit.returnPressed.connect(self.onOkClicked)
        
        self.old_psdEdit.setFocus()
        
        # 提交按钮
        btn = QPushButton('OK', self)
        btn.clicked.connect(self.onOkClicked)
        btn.setAutoDefault(False)
        btn.setDefault(False)
        
        # 设置文字样式
        font = QFont()
        font.setPixelSize(16)
        
        old_psd_lbl.setFont(font)
        new_psd_lbl.setFont(font)
        new_psd_repeat_lbl.setFont(font)
        
        self.old_psdEdit.setFont(font)
        self.new_psdEdit.setFont(font)
        self.new_psd_repeatEdit.setFont(font)

        btn.setFont(font)
        
        # 提交按钮水平居中
        hbox = QHBoxLayout()
        hbox.addStretch(1)
        hbox.addWidget(btn)
        hbox.addStretch(1)
        
        # 表格排列
        grid = QGridLayout()
        grid.addWidget(old_psd_lbl, 0, 0)
        grid.addWidget(self.old_psdEdit, 0, 1)
        grid.addWidget(new_psd_lbl, 1, 0)
        grid.addWidget(self.new_psdEdit, 1, 1)
        grid.addWidget(new_psd_repeat_lbl, 2, 0)
        grid.addWidget(self.new_psd_repeatEdit, 2, 1)
        grid.addLayout(hbox, 3, 0, 1, 2)
        
        self.setLayout(grid)
       
    def onOkClicked(self):
        old_psd = self.old_psdEdit.text()
        new_psd = self.new_psdEdit.text()
        new_psd_repeat = self.new_psd_repeatEdit.text()
        
        if old_psd.strip() == "":  # 检查 websiteEdit 是否为空（或只包含空白字符）
            QMessageBox.warning(self, "提示", "请输入旧密码")
            return
        if new_psd.strip() == "":
            QMessageBox.warning(self, "提示", "请输入新密码")
            return
        if new_psd_repeat.strip() == "":
            QMessageBox.warning(self, "提示", "请再次输入新密码")
            return
            
        if new_psd != new_psd_repeat:
            QMessageBox.warning(self, "错误", "新密码不一致")
            return

        self.accept()  # 如果 QLineEdit 中有文本，则接受对话框（关闭并返回 QDialog.Accepted）
     
