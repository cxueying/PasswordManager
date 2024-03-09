from PyQt6.QtWidgets import QWidget, QGridLayout, QTableWidget,QTableWidgetItem, QPushButton, QSpacerItem, QSizePolicy, QApplication, QHBoxLayout
from manage.manage_psd import PasswordManager
from gui.dialog.psd_input_dialog import PSDInputDialog


manage = PasswordManager()

class PSDManagePage(QWidget):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.initUI()
        
    def initUI(self):
        self.grid_layout = QGridLayout()
        self.table = QTableWidget(self)
        self.grid_layout.addWidget(self.table, 0, 0)
        
        self.fresh_psd_table()
        self.add_Password_button()
        self.table.cellClicked.connect(self.copy_cell_content)
        self.setLayout(self.grid_layout)
        
    
    def fresh_psd_table(self):
        results = manage.get_all_password()
        self.table.setRowCount(0)
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(["网站", "用户名", "密码", "显示", "删除"])

        # 不允许修改表格内容
        self.table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        
        i = 0
        for result in results:
            self.table.insertRow(i)
            self.table.setItem(i, 0, QTableWidgetItem(result["website"]))
            self.table.setItem(i, 1, QTableWidgetItem(result["username"]))
            self.table.setItem(i, 2, QTableWidgetItem('********'))
            
            # 添加一个显示密码的按钮
            show_btn = QPushButton('Show', self)
            show_btn.clicked.connect(lambda _, row=i, password=result["password"], btn=show_btn: self.show_password(row, password, btn))
            self.table.setCellWidget(i, 3, show_btn)
            
            # 添加一个删除按钮
            btn = QPushButton('Delete', self)
            btn.clicked.connect(lambda _, row=i: self.delete_row(row))
            self.table.setCellWidget(i, 4, btn)
            
            i += 1
        
    
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
            manage.add_password(dialog.websiteEdit.text(), dialog.usernameEdit.text(), dialog.psdEdit.text())
            self.fresh_psd_table()
        
        
    def delete_row(self, row):
        website = self.table.item(row, 0).text()
        username = self.table.item(row, 1).text()
        print(website)
        print(username)
        
        manage.delete_password(website, username)
        
        self.fresh_psd_table()
        
        
    def show_password(self, row, password, btn):
        password_item = self.table.item(row, 2)
        if password_item.text() == password:
            password_item.setText('********')
            btn.setText('Show')
        else:
            password_item.setText(password)
            btn.setText('Hide')
        
        
    def copy_cell_content(self, row, column):
        if column <=2:
            cell_content = self.table.item(row, column).text()
            QApplication.clipboard().setText(cell_content)
            self.parent.statusBar.showMessage("复制成功", 2000)


