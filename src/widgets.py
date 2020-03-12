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
        indeces = list(range(self.row_count))
        for idx in indeces[::-1]:
            item = self.takeItem(idx)
            del item
            self.row_count -= 1
        return True


class LoadTorrentButton(QPushButton):
    def __init__(self,txt,parent=None):
        super().__init__(self,txt,parent=parent)

    @classmethod
    def create(cls,window=None,listWidget=None,combo=None,txt=None):
        btn = cls(txt,parent=None)
        btn.label = txt
        btn.window = window
        btn.listWidget = listWidget
        btn.combo = combo
        btn.clicked.connect(show_info)
        return btn

    def check_if_empty(self):
        return self.window.torrentList.isEmpty()

    def show_info(self):
        window = self.window
        self.check_if_empty()
        session_name = window.combo.currentText()
        session = window.manager.pull_session()
        for  in session.models:
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

    def set_header(self,txt):
        self.addItem(txt)


class ListItem(QListWidgetItem):
    def __init__(self,txt):
        super().__init__(txt)
        self._hash = None
        self._session = None

    @property
    def torrent_hash(self):
        if self._hash:
            return self._hash
        return

    @torrent_hash.setter
    def torrent_hash(self,torrent_hash):
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

    def create(self)
