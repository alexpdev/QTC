from PyQt5.QtWidgets import QComboBox, QFrame, QListWidgetItem, QTableWidget, QTableWidgetItem,QPushButton,QListWidget

from PyQt5.QtGui import QFont

class TableWidget(QTableWidget):
    def __init__(self,parent=None):
        super().__init__(parent=parent)
        self.parent = parent
        self.setObjectName(u"tableWidget")
        self.setFrameShape(QFrame.WinPanel)
        self.setFrameShadow(QFrame.Sunken)
        self.setLineWidth(4)
        self.setMidLineWidth(6)

    @classmethod
    def create(cls,model):
        pass

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
        for idx in range(self.row_count):
            item = self.takeItem(idx)
            del item
        return True


class LoadTorrentButton(QPushButton):
    def __init__(self,txt,parent=None):
        super().__init__(self,txt,parent=parent)

    @classmethod
    def create(cls,mainwindow=None,txt=None,parent=None):
        ltb = cls(txt,parent=parent)
        ltb.main = mainwindow
        ltb.clicked.connect(show_info)
        return ltb

    def checkListEmpty(self):
        self.main.checkListEmpty(self.main.torrentList)

    def show_info(self):
        self.checkListEmpty()
        name = self.combo.currentText()
        session = self.man.sessions[name]
        for hash_ in session.models:
            torrent_name = session.models[hash_][0].name
            item = ListItem(torrent_name)
            item.hash_ = hash_
            item.session = name
            item.setForeground(self.fg_brush)
            item.setBackground(self.bg_brush)
            item.setFont(self.fancyfont)
            self.torrentList.addItem(item)
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
        self.comboDict = {}

    def addToDict(self,session,txt):
        if session.name in self.comboDict:
            self.comboDict[session.name].append(txt)
        else:
            self.comboDict[session.name] = [txt]
        return

    def name_in_dict(self,name):
        if name in self.comboDict:
            return self.comboDict[name]
        return False

    def set_dict_header(self,txt):
        if txt not in self.comboDict:
            self.comboDict[txt] = []
            self.addItem(txt)


class ListItem(QListWidgetItem):
    def __init__(self,txt):
        super().__init__(txt)
        self._hash = None
        self._session = None

    @property
    def hash_(self):
        if self._hash:
            return self._hash
        return

    @hash_.setter
    def hash_(self,_hash):
        if not self._hash:
            self._hash = _hash
        return

    @property
    def session(self):
        if self._session:
            return self._session
        return

    @session.setter
    def session(self,session):
        if not self._session:
            self._session = session
        return
