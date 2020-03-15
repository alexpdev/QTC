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


class TorrentList(ListWidget):
    def __init__(self, parent=None):
        super().__init__(parent=parent)

    def assign(self,session,staticWidg,tableWidg):
        self.session = session
        self.staticWidg = staticWidg
        self.tableWidg = tableWidg

    def display_info(self):
        self.staticWidg.isempty()
        selected = self.currentItem()
        torHash = selected.torHash
        client = selected.client
        self.get_data_table_fields(torHash,client)
        data = self.session.get_static_fields(torHash,client)
        for pair in data:
            entry = "  ||  ".join(pair)
            item = ListItem(entry)
            item.setForeground(self.fg_brush)
            item.setBackground(self.bg_brush)
            item.setFont(self.sansfont)
            self.static_info.appendItem(item)

    def get_data_table_fields(self,torHash,client):
        values = self.session.get_data_fields(torHash,client)


    # def comparable_fields(self, models):
    #     v_headers,rows,cols = [],len(models),None
    #     for i,model in enumerate(models):
    #         fields = model.tableFields()
    #         v_headers.append(str(fields["Timestamp"]))
    #         del fields["Timestamp"]
    #         if not cols:
    #             cols = len(fields)
    #             h_headers = [str(j) for j in fields.keys() if j != "Timestamp"]
    #             cells = [[] for j in range(len(models))]
    #         for x,header in enumerate(fields):
    #             item = QTableWidgetItem(str(fields[header]))
    #             item.setForeground(self.fg_brush)
    #             item.setBackground(self.bg_brush)
    #             item.setFont(self.sansfont)
    #             item.setFlags(Qt.ItemIsSelectable|Qt.ItemIsUserCheckable|Qt.ItemIsEnabled)
    #             cells[i].append(item)
    #     self.table_data.setRowCount(rows)
    #     self.table_data.setColumnCount(cols)
    #     self.table_data.setHorizontalHeaderLabels(h_headers)
    #     self.table_data.setVerticalHeaderLabels(v_headers)
    #     for x,row in enumerate(cells):
    #         for y,item in enumerate(row):
    #             self.table_data.setItem(x,y,cells[x][y])


class StaticButton(QPushButton):
    def __init__(self,txt,parent):
        super().__init__(txt,parent)

    def assign(self,combo,session,listwidget):
        self.listwidget = listwidget
        self.combo = combo
        self.session = session
        self.clicked.connect(self.show_info)

    def check_if_empty(self):
        return self.listWidget.isEmpty()

    def show_info(self):
        self.check_if_empty()
        session_name = self.combo.currentText()
        for item in self.session.get_torrent_names():
            name,torrent_hash,client = item
            item = ListItem.create(*item)
            item.setForeground(self.window.fg_brush)
            item.setBackground(self.window.bg_brush)
            item.setFont(self.window.fancyfont)
            self.listwidget.addItem(item)
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
            self.addItem("client")
        return

class ListItem(QListWidgetItem):
    def __init__(self,name):
        super().__init__(name)

    @classmethod
    def create(cls,name,thash,client):
        item = cls(name)
        item.label = name
        item.client = client
        item.torHash = thash
        return item
