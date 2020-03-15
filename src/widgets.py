import itertools
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import (QComboBox, QFrame, QListWidget, QListWidgetItem,
                             QPushButton, QTableWidget, QTableWidgetItem)


class TableWidget(QTableWidget):
    def __init__(self,parent=None):
        super().__init__(parent=parent)
        self.parent = parent
        self.setObjectName(u"tableWidget")
        self.setFrameShape(QFrame.WinPanel)
        self.setFrameShadow(QFrame.Sunken)
        self.setLineWidth(4)
        self.setMidLineWidth(6)



class ListWidget(QListWidget):
    def __init__(self,parent=None):
        super().__init__(parent=parent)
        self.row_count = 0
        self.setSpacing(2)

    def appendItem(self,item):
        self.addItem(item)
        self.row_count += 1

    def isEmpty(self):
        self.clear()
        indeces = list(range(self.row_count))
        for idx in indeces[::-1]:
            item = self.takeItem(idx)
            del item
            self.row_count -= 1
        return True


class TorrentNames(ListWidget):
    def __init__(self, parent=None):
        super().__init__(parent=parent)

    def assign(self,session,static,table):
        self.session = session
        self.static = static
        self.table = table
        self.itemSelectionChanged.connect(self.display_info)

    def display_info(self):
        self.static.isempty()
        selected = self.currentItem()
        t_hash = selected.t_hash
        client = selected.client
        self.pull_static_from_db(t_hash,client)
        self.pull_data_from_db(t_hash,client)

    def pull_data_from_db(self,t_hash,client):
        db_rows = self.session.get_data_rows(t_hash,client)
        headers,rows,cols = None,len(db_rows),None
        model = db_rows[0]
        headers = tuple(k for k,v in model)
        cols = len(headers)
        self.table_data.setRowCount(rows)
        self.table_data.setColumnCount(cols)
        self.table_data.setHorizontalHeaderLabels(headers)
        for x,row in enumerate(db_rows):
            for y,value in enumerate(row):
                self.table_data.setItem(x,y,value[1])
        return

    def pull_static_from_db(self,t_hash,client):
        values = self.session.get_static_rows(t_hash,client)
        for entry in itertools.chain.from_iterable(values):
            item = ListItem(entry)
            item.setForeground(self.fg_brush)
            item.setBackground(self.bg_brush)
            item.setFont(self.sansfont)
            self.static.appendItem(item)
        return


class StaticButton(QPushButton):
    def __init__(self,txt,parent):
        super().__init__(txt,parent)

    def assign(self,combo,session,torrentNames):
        self.combo = combo
        self.session = session
        self.torrentNames = torrentNames
        self.clicked.connect(self.show_info)

    def show_info(self):
        self.torrentNames.check_if_empty()
        session_name = self.combo.currentText()
        for item in self.session.get_torrent_names(session_name):
            name,torrent_hash,client = item
            item = ListItem.create(*item)
            item.setForeground(self.window.fg_brush)
            item.setBackground(self.window.bg_brush)
            item.setFont(self.window.fancyfont)
            self.torrentNames.addItem(item)
        return


class CustomFont(QFont):
    info = {}
    def __init__(self):
        super().__init__()
        self.assign()

    def assign(self):
        self.setFamily(self.info["name"])
        self.setPointSize(self.info["size"])
        self.setBold(self.info["bold"])



class FancyFont(CustomFont):
    info = {"name":"Leelawadee","size":11,"bold":False}
    def __init__(self):
        super().__init__()


class SansFont(CustomFont):
    info = {"name":"Dubai Medium","size":11,"bold":True}
    def __init__(self):
        super().__init__()



class ComboBox(QComboBox):
    def __init__(self, parent=None):
        super().__init__(parent=parent)

    def assign(self,session):
        self.session = session
        for client in self.session.get_client_names():
            self.addItem(client)
        return


class ListItem(QListWidgetItem):
    def __init__(self,name):
        super().__init__(name)

    @classmethod
    def create(cls,name,t_hash,client):
        item = cls(name)
        item.label = name
        item.t_hash = t_hash
        item.client = client
        return item
