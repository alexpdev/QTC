from PyQt5.QtWidgets import QComboBox,QPushButton,QTreeWidgetItem

class ComboBox(QComboBox):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.comboDict = {}

    def addToDict(self,session,item):
        if session.name in self.comboDict:
            self.comboDict[session.name].append(item)
        else:
            self.comboDict[session.name] = [item]
        return

    def name_in_dict(self,name):
        if name in self.comboDict:
            return self.comboDict[name]
        return False


class ListItem(QListWidgetItem):
    def __init__(self,txt):
        super().__init__(txt)
        self.hash_ = None

    def setHash(self,hash_):
        self.hash_ = hash_

    def getHash(self):
        return self.hash_
