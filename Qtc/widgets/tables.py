from PyQt5.QtWidgets import QTableView
from PyQt5.QtGui import QStandardItem, QStandardItemModel
from PyQt5.QtCore import Qt

class TableView(QTableView):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.window = parent
        self.checks = []
        self.setShowGrid(True)


    def assign(self,session,window):
        self.window = window
        self.session = session
        self.menubar = window.menubar
        self.itemModel = ItemModel(parent=self)
        self.itemModel.setSession(self.session)
        self.setModel(self.itemModel)
        return

    def get_columns(self):
        col = self.itemModel.col_map
        return col

    def get_rows(self):
        row = self.itemModel.row_map
        return row

    def check_menus(self):
        for field,idx in self.checks:
            self.setRowHidden(idx,True)
        return

class ItemModel(QStandardItemModel):
    def __init__(self,parent=None):
        super().__init__(parent=None)
        self.view = parent
        self.row_count = 0
        self.flags = (Qt.ItemIsSelectable|Qt.ItemIsEnabled)
        self.chartView = None

    def setSession(self,session):
        self.session = session
        self.window = session.win
        self.row_map = session.static_fields
        self.col_map = session.data_fields
        return

    def receive_static(self,data):
        self.isEmpty()
        row = data[0]
        self.setColumnCount(1)
        self.setRowCount(len(row))
        headers = self.session.get_headers(self.row_map)
        self.setVerticalHeaderLabels(headers)
        for field in self.row_map:
            item = self.session.gen_items(field,row[field])
            self.setItem(self.row_count,0,item)
            self.row_count += 1
        self.view.resizeColumnsToContents()
        return

    def receive_table(self,data):
        self.isEmpty()
        first = data[0]
        self.setColumnCount(len(first))
        self.setRowCount(len(data))
        headers = self.session.get_headers(self.col_map)
        self.setHorizontalHeaderLabels(headers)
        for x,row in enumerate(data):
            for y,field in enumerate(self.col_map):
                item = self.session.gen_items(field,row[field])
                self.setItem(x,y,item)
            self.row_count += 1
        self.view.check_menus()
        return

    def isEmpty(self):
        self.clear()
        indeces = list(range(self.row_count))
        for idx in indeces[::-1]:
            item = self.takeRow(idx)
            del item
            self.row_count -= 1
        return True


class StandardItem(QStandardItem):
    def __init__(self,txt):
        super().__init__(txt)
        self.display_value = txt
        self.value = None
        self.label = None
        self.field = None

    def set_label(self,arg):
        self.label = arg

    def set_display_value(self,arg):
        self.display_value = arg

    def set_value(self,arg):
        self.value = arg

    def set_field(self,arg):
        self.field = arg
