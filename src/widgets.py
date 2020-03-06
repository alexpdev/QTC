from PyQt5.QtWidgets import QComboBox,QListWidgetItem

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
