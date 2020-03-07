import sys
from PyQt5.QtWidgets import (QLabel, QMenu, QWidget, QMenuBar,
                             QStatusBar, QMainWindow, QListWidget, QVBoxLayout, QHBoxLayout, QPushButton, QTableWidget, QApplication, QListWidgetItem, QTableWidgetItem)
from PyQt5.QtGui import QFont
from src.widgets import ListItem, ComboBox, CentaurFont


class Win(QMainWindow):

    def __init__(self, parent=None):
        super().__init__(parent=parent)

        # Main Window Frame
        self.resize(1400, 800)
        self.setWindowTitle("Torrent Companion")
        centralWidget = QWidget(self)
        menubar = self.menuBar()
        # self.satusBar.showMessage('Ready')
        file_menu = QMenu("File",menubar)
        quitaction = file_menu.addAction("Quit")
        quitaction.triggered.connect(self.destroy_something)
        menubar.addMenu(file_menu)
        # menu.addMenu(file_menu)
        help_menu = QMenu("Edit",menubar)
        print_action = help_menu.addAction("Print")
        print_action.triggered.connect(self.print_something)
        menubar.addMenu(help_menu)
        # menu.addMenu(help_menu)
        self.setCentralWidget(centralWidget)
        font = QFont("Leelawadee")
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

    def print_something(self):
        print("I have been clicked")

    def destroy_something(self):
        self.destroy()
        sys.exit(app.exec_())

    def show_torrent_info(self):
        selected = self.torrents.currentItem()
        print(selected)
        models = self.man.get_models(selected.session,selected.hash_)
        print(len(models))
        self.checkListEmpty(self.general)
        self.comparable_fields(models)
        fields = models[0].static_fields()
        for k,v in fields.items():
            txt = k + "  :  " + v
            item = ListItem(txt)
            self.general.addItem(item)

    def comparable_fields(self, models):
        cols,rows = len(models),None
        column_headers,row_headers = [],[]
        cells = []
        for model in models:
            fields = model.tableFields()
            if not rows:
                rows = len(fields)
                row_headers = [i for i in fields.keys()]
                cells = [[] for i in range(rows)]
            for x,header in enumerate(fields):
                item = QTableWidgetItem(fields[header])
                cells[x].append(item)
        self.table.setRowCount(rows)
        self.table.setColumnCount(cols)
        self.table.setHorizontalHeaderLabels(column_headers)
        self.table.setVerticalHeaderLabels(row_headers)
        for x,row in enumerate(cells):
            for y,item in enumerate(row):
                self.table.setItem(x,y,cells[x][y])

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
