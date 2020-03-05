import sys
import os
import json
import string
from datetime import datetime
from PyQt5.QtWidgets import      (   QLabel,
                                      QMenu,
                                     QFrame,
                                    QTabBar,
                                    QWidget,
                                   QMenuBar,
                                  QComboBox,
                                  QDateEdit,
                                 QStatusBar,
                                 QTabWidget,
                                QMainWindow,
                                QListWidget,
                                QVBoxLayout,
                                QHBoxLayout,
                                QGridLayout,
                                QColumnView,
                                QPushButton,
                                QTreeWidget,
                               QTableWidget,
                               QApplication,
                            QTreeWidgetItem,
                            QListWidgetItem,
)
from PyQt5.QtGui import QFont
from src.listItem import ListItem

class Win(QMainWindow):

    def __init__(self,master=None):
        super().__init__(master)

        # Main Window Frame
        self.master = master
        self.setWindowTitle("Torrent Companion")
        self.resize(900,700)
        centralWidget = QWidget(self)
        widg = QWidget(centralWidget)
        font = QFont()
        menu = QMenuBar(centralWidget)
        menu.setNativeMenuBar(True)
        menu.setGeometry(2,2,50,898)
        status = QStatusBar(centralWidget)
        menu.setGeometry(670,2,698,898)
        file_menu = QMenu("&File")
        edit_menu = QMenu("&Edit")
        menu.addMenu(file_menu)
        menu.addMenu(edit_menu)
        font.setPointSize(11)
        font.setBold(False)
        centralWidget.setFont(font)
        widg.resize(870,650)
        self.setMenuBar(menu)
        self.setStatusBar(status)
        self.setCentralWidget(centralWidget)
        self.btn1 = QPushButton("Load Info",centralWidget)
        self.combo = QComboBox()
        self.torrents = QListWidget(centralWidget)
        vLay = QVBoxLayout()
        vLay.addWidget(self.torrents)
        vLay.addWidget(self.combo)
        vLay.addWidget(self.btn1)
        self.general = QListWidget(centralWidget)
        self.table = QTableWidget(centralWidget)
        hLay = QHBoxLayout()
        hLay.addLayout(vLay)
        hLay.addWidget(self.general)
        hLay.addWidget(self.table)
        widg.setLayout(hLay)
        # self.btn1.clicked.connect(self.show_info)

    def show_info(self):
        if not self.combodict:
            self.combodict = {}
        name = self.combo.currentText()
        if name:
            if name not in self.combodict:
                self.combodict[name] = []
            for child in self.torrents.children():
                item = self.torrents.takeItem()
                self.combodict[name].append(item)

        session = next(i for i in self.man.sessions if i.name == name)
        for hash_ in session.models:
            torrent_name = session.models[hash_][0].name
            item = ListItem(torrent_name)
            item.setHash(hash_)
            self.torrents.addItem(item)
        return


    def set_session_manager(self,manager):
        self.man = manager
        for session in self.man.sessions:
            self.combo.addItem(session.name)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = Win()
    win.show()
    sys.exit(app.exec_())
