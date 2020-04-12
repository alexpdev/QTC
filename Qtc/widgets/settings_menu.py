from PyQt5.QtWidgets import (QWidget, QPushButton, QDialogButtonBox, QTabWidget,
                             QLabel, QFormLayout, QLineEdit, QDialog)

from qtc.widgets.fonts import Cambria

class SettingsMenu(QDialog):
    def __init__(self,window=None,session=None,parent=None):
        super().__init__(parent=parent)
        self.window = window
        self.session = session
        self.setObjectName("SettingsMenu")
        self.setWindowTitle("Settings")
        self.setupUi()
        font = Cambria()
        self.setFont(font)
        self.setStyleSheet("QPushButton{padding: 6px; margin: 2px;} QLabel{margin: 8px; padding: 2px;} QLineEdit{padding: 2px; margin: 5px; border: 1px solid black;}")

    def setupUi(self):
        submit_btn = QPushButton("Submit",parent=self)
        submit_btn.setDefault(True)
        cancel_btn = QPushButton("Cancel",parent=self)
        label1 = QLabel("Client Name")
        label1.setObjectName("ClientLabel")
        label2 = QLabel("Client URL")
        label2.setObjectName("UrlLabel")
        label3 = QLabel("Username")
        label3.setObjectName("UsernameLabel")
        label4 = QLabel("Password")
        label4.setObjectName("PasswordLabel")
        edit1 = QLineEdit(parent=self)
        edit1.setObjectName("Client")
        edit2 = QLineEdit(parent=self)
        edit2.setObjectName("UrlEdit")
        edit3 = QLineEdit(parent=self)
        edit3.setObjectName("UsernameEdit")
        edit4 = QLineEdit(parent=self)
        edit4.setObjectName("PasswordEdit")
        layout = QFormLayout(parent=self)
        layout.setObjectName("Layout")
        self.setLayout(layout)
        layout.addRow(label1,edit1)
        layout.addRow(label2,edit2)
        layout.addRow(label3,edit3)
        layout.addRow(label4,edit4)
        layout.addRow(submit_btn,cancel_btn)
        submit_btn.clicked.connect(self.submit_fields)
        cancel_btn.clicked.connect(self.cancel_form)

    def submit_fields(self):
        pass

    def cancel_form(self):
        self.destroy()

