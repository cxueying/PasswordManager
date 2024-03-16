from PyQt6.QtWidgets import QWidget, QGridLayout, QTableWidget,QTableWidgetItem, QPushButton, QApplication, QHBoxLayout, QMessageBox, QAbstractItemView
from PyQt6.QtGui import QIcon, QDesktopServices
from gui.dialog.psd_input_dialog import PSDInputDialog
from PyQt6.QtCore import Qt, QSize, QUrl
from manage.passwords import PSDManager
from manage.users import UsersManage


class PSDManagePage(QWidget):
    def __init__(self, parent):
        super().__init__()
        self.user_manage = UsersManage()
        self.psd_manage = PSDManager()
        
        self.parent = parent
        self.user = self.user_manage.get_login()
        
        self.initUI()

        
    def initUI(self):
        self.grid_layout = QGridLayout()
        self.table = QTableWidget(self)
        self.table_init()
        self.grid_layout.addWidget(self.table, 0, 0)
        
        self.fresh_psd_table()
        self.add_Password_button()
        self.table.cellClicked.connect(self.cell_clicked)
        self.setLayout(self.grid_layout)
        
    def table_init(self):
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(["网站", "用户名", "密码", "显示密码", "删除"])
        # 不允许修改表格内容
        self.table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)

        
        self.table.setColumnWidth(0, 200)
        
    
    def fresh_psd_table(self):
        self.table.setRowCount(0)
        results = self.psd_manage.get(self.user)
        if results == None:
            return 
        
        i = 0
        for result in results:
            self.table.insertRow(i)
            websiteItem = QTableWidgetItem(result["website"])
            websiteItem.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            
            usernameItem = QTableWidgetItem(result["account"])
            usernameItem.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            
            passwordItem = QTableWidgetItem('********')
            passwordItem.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            
            self.table.setItem(i, 0, websiteItem)
            self.table.setItem(i, 1, usernameItem)
            self.table.setItem(i, 2, passwordItem)
            
            # 添加一个显示密码的按钮
            show_btn = QPushButton(self.table)
            show_btn.setIcon(QIcon(r".\assets\icon\show.png"))
            show_btn.setIconSize(QSize(32, 32))
            show_btn.clicked.connect(lambda _, row=i, password=result["password"], btn=show_btn: self.show_password(row, password, btn))
            self.table.setCellWidget(i, 3, show_btn)
            
            # 添加一个删除按钮
            btn = QPushButton(self)
            btn.setIcon(QIcon(r'.\assets\icon\delete.png'))
            btn.setIconSize(QSize(32, 32))
            btn.clicked.connect(lambda _, row=i: self.delete_row(row))
            self.table.setCellWidget(i, 4, btn)
            
            i += 1
            
        for row in range(self.table.rowCount()):
            self.table.setRowHeight(row, 50)
        
        
    
    def add_Password_button(self):
        add_button = QPushButton("添加密码")
        add_button.setMaximumSize(100, 50)
        add_button.setMinimumSize(100, 50)
        add_button.clicked.connect(self.add_button_clicked)
        
        hbox = QHBoxLayout()
        hbox.addStretch(1)
        hbox.addWidget(add_button)
        hbox.addStretch(1)
        
        self.grid_layout.addLayout(hbox, 1, 0)
        
        
    def add_button_clicked(self):
        
        dialog = PSDInputDialog()
        if dialog.exec():
            if self.psd_manage.add(self.user, dialog.websiteEdit.text(), dialog.usernameEdit.text(), dialog.psdEdit.text()) == False:
                QMessageBox.warning(self, "错误", "添加密码失败")
            self.fresh_psd_table()
            self.setStatusBar("添加密码成功", 2000)
        
        
    def delete_row(self, row):
        website = self.table.item(row, 0).text()
        account = self.table.item(row, 1).text()
        
        reply = QMessageBox.question(
            self,
            "提示",
            "确定删除该信息吗？",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )
        if reply == QMessageBox.StandardButton.Yes:
            self.psd_manage.delete(self.user, website, account)
            self.fresh_psd_table()
            self.setStatusBar("删除密码成功", 2000)
        
        
    def show_password(self, row, password, btn):
        password_item = self.table.item(row, 2)
        if password_item.text() == self.psd_manage.decrypt(password):
            password_item.setText('********')
            btn.setIcon(QIcon(r".\assets\icon\show.png"))
        else:
            password_item.setText(self.psd_manage.decrypt(password))
            btn.setIcon(QIcon(r".\assets\icon\hide.png"))
        
        
    def cell_clicked(self, row, column):
        if column ==0:
            url = self.table.item(row, column).text()
            QDesktopServices.openUrl(QUrl(url))
        elif column == 1 or column == 2:
            cell_content = self.table.item(row, column).text()
            QApplication.clipboard().setText(cell_content)
            self.setStatusBar("复制成功", 2000)
            
    def setStatusBar(self, message, time):
        self.parent.statusBar.showMessage(message, time)

