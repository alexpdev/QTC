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

    def assign(self,manager,mainwindow,table,staticlist):
        self.main = mainwindow
        self.table = table
        self.static = staticlist
        self.manager = manager
        return

    def show_torrent_info(self):
        self.static.isEmpty()
        selected = self.currentItem()
        if selected.model.has_items():
            models = selected.model.data_models
        else:
            self.manager
        fields = models[0].static_fields()
        for k,v in fields.items():
            txt = str(k) + "  :||:  " + str(v)
            item = ListItem(txt)
            item.setForeground(self.fg_brush)
            item.setBackground(self.bg_brush)
            item.setFont(self.sansfont)
            self.static_info.appendItem(item)

    def comparable_fields(self, models):
        v_headers,rows,cols = [],len(models),None
        for i,model in enumerate(models):
            fields = model.tableFields()
            v_headers.append(str(fields["Timestamp"]))
            del fields["Timestamp"]
            if not cols:
                cols = len(fields)
                h_headers = [str(j) for j in fields.keys() if j != "Timestamp"]
                cells = [[] for j in range(len(models))]
            for x,header in enumerate(fields):
                item = QTableWidgetItem(str(fields[header]))
                item.setForeground(self.fg_brush)
                item.setBackground(self.bg_brush)
                item.setFont(self.sansfont)
                item.setFlags(Qt.ItemIsSelectable|Qt.ItemIsUserCheckable|Qt.ItemIsEnabled)
                cells[i].append(item)
        self.table_data.setRowCount(rows)
        self.table_data.setColumnCount(cols)
        self.table_data.setHorizontalHeaderLabels(h_headers)
        self.table_data.setVerticalHeaderLabels(v_headers)
        for x,row in enumerate(cells):
            for y,item in enumerate(row):
                self.table_data.setItem(x,y,cells[x][y])


class StaticButton(QPushButton):
    def __init__(self,txt,parent):
        super().__init__(txt,parent)

    @classmethod
    def create(cls,window,listWidget,combo,txt,parent):
        btn = cls(txt,parent)
        btn.label = txt
        btn.window = window
        btn.listWidget = listWidget
        btn.combo = combo
        btn.clicked.connect(btn.show_info)
        return btn

    def check_if_empty(self):
        return self.listWidget.isEmpty()

    def get_manager(self):
        return self.window.manager

    def show_info(self):
        self.check_if_empty()
        session_name = self.combo.currentText()
        manager = self.get_manager()
        for model in manager.iter_session_models(session_name):
            args = (model.name, model.torrent_hash, model.client)
            item = ListItem.create(*args)
            item.setForeground(self.window.fg_brush)
            item.setBackground(self.window.bg_brush)
            item.setFont(self.window.fancyfont)
            self.listWidget.addItem(item)
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



class ListItem(QListWidgetItem):
    def __init__(self,model):
        super().__init__(model.name)
        self.label = model.name
        self.torrent_hash = model.torrent_hash
        self.model = model
        self.client = model.client
