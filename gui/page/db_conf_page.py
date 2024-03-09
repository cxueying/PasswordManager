from PyQt6.QtWidgets import QWidget, QLabel, QVBoxLayout

class DBConfPage(QWidget):
    def __init__(self, ):
        super().__init__()
        self.initUI()
        
    def initUI(self):
        self.setMinimumSize(200, 200)  # 设置最小大小
        layout = QVBoxLayout()
        label = QLabel('数据库配置界面')
        layout.addWidget(label)
        self.setLayout(layout)