import sys
from PyQt5.QtWidgets import (QLabel, QMenu, QWidget, QMenuBar,
                             QStatusBar, QMainWindow, QListWidget, QVBoxLayout, QHBoxLayout, QPushButton, QTableWidget, QApplication, QListWidgetItem, QTableWidgetItem)
from PyQt5.QtGui import QFont
from src.widgets import ListItem, ComboBox, CentaurFont


class Win(QMainWindow):

    def __init__(self, parent=None):
        super().__init__(parent=parent)

        # Main Window Frame
        self.resize(1100, 800)
        self.setWindowTitle("Torrent Companion")
        centralWidget = QWidget(self)
        self.setCentralWidget(centralWidget)
        self.status = QStatusBar(self)
        self.menu = QMenuBar(self)
        self.setMenuBar(self.menu)
        self.setStatusBar(self.status)
        file_menu = QMenu("&File")
        help_menu = QMenu("&Help")
        self.menu.addMenu(file_menu)
        self.menu.addMenu(help_menu)
        self.loadLogs = file_menu.addAction("Import Logs")
        self.about = file_menu.addAction("About")
        self.menu.setNativeMenuBar(True)
        self.menu.setGeometry(2, 2, 50, 898)
        self.status.setGeometry(670, 2, 698, 898)
        font = QFont()
        font.setPointSize(10)
        font.setBold(False)
        centralWidget.setFont(font)
        self.btn1 = QPushButton("Load Info", centralWidget)
        self.btn2 = QPushButton("Load Torrent Info", centralWidget)
        self.combo = ComboBox()
        self.combo.setEditable(False)
        self.torrents = QListWidget(centralWidget)
        self.torrents.setSpacing(2)
        vLay = QVBoxLayout()
        vLay.addWidget(self.btn2)
        vLay.addWidget(self.torrents)
        vLay.addWidget(self.combo)
        vLay.addWidget(self.btn1)
        vLay.setSpacing(6)
        widg = QWidget()
        self.general = QListWidget(widg)
        self.general.setSpacing(6)
        self.general.setFont(font)
        self.table = QTableWidget(widg)
        self.table.setFont(font)
        vLay2 = QVBoxLayout()
        vLay2.setSpacing(4)
        vLay2.addWidget(self.general)
        vLay2.addWidget(self.table)
        widg.setLayout(vLay2)
        hLay = QHBoxLayout()
        hLay.addLayout(vLay)
        hLay.addWidget(widg)
        hLay.setSpacing(5)
        centralWidget.setLayout(hLay)
        self.btn1.clicked.connect(self.show_info)
        self.btn2.clicked.connect(self.show_torrent_info)

    def show_torrent_info(self):
        current_item = self.torrents.currentItem()
        curItemHash,curItemSes = current_item.hash_,current_item.session
        models = self.man.sessions[curItemSes].models[curItemHash]
        fields = models[0].static_fields()
        self.checkListEmpty(self.general)
        for k,v in fields.items():
            txt = k + "  :  " + v
            item = ListItem(txt)
            self.general.addItem(item)
        self.comparable_fields(models)

    def comparable_fields(self, models):
        vheaders,hheaders = [],[]
        table = []
        for model in models:
            row = []
            f = model.get_comparable_fields()
            for k,v in f.items():
                item = QTableWidgetItem(v)
                row.append(item)
                if not table:
                    vheaders.append(k)
            table.append(row)
            hheaders.append(str(model.logtime))
        self.table.setRowCount(len(vheaders))
        self.table.setColumnCount(len(hheaders))
        self.table.setHorizontalHeaderLabels(hheaders)
        self.table.setVerticalHeaderLabels(hheaders)
        for x,row in enumerate(table):
            for y,item in enumerate(row):
                self.table.setItem(x,y,table[x][y])

    def show_info(self):
        self.checkListEmpty(self.torrents)
        name = self.combo.currentText()
        session = self.man.sessions[name]
        itemFont = CentaurFont()
        for hash_ in session.models:
            torrent_name = session.models[hash_][0].name
            item = ListItem(torrent_name)
            item.hash_ = hash_
            item.session = name
            item.setFont(itemFont)
            self.torrents.addItem(item)
        return

    def checkListEmpty(self, widget):
        for idx in range(widget.count()):
            item = widget.takeItem(idx)
            del item
        return

    def set_session_manager(self, manager):
        self.man = manager
        for session in self.man.sessions:
            self.combo.set_dict_header(session)
            self.man.sessions[session].load_models()
        return


if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = Win()
    win.show()
    sys.exit(app.exec_())
