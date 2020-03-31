from PyQt5.QtWidgets import QTreeWidget, QTreeWidgetItem
from qtc.widgets.fonts import Cambria, Dubai


class TreeWidget(QTreeWidget):
    stylesheet = ""
    def __init__(self,parent=None):
        super().__init__(parent=parent)
        self.setAlternatingRowColors(True)
        self.setAnimated(True)
        self.setStyleSheet("margin-top: 10px; margin-bottom: 10px;")
        self.setIndentation(18)
        self.setUniformRowHeights(True)
        self.setHeaderHidden(True)
        self.setColumnCount(1)

    def assign(self,session=None,window=None):
        self.session = session
        self.window = window
        self.table = window.dataTable
        self.static = window.staticTable
        self.add_top_items()
        self.itemSelectionChanged.connect(self.display_info)
        return

    def add_top_items(self):
        for client in self.session.get_client_names():
            top_item = TopTreeItem(0,client,self.session)
            self.addTopLevelItem(top_item)
            client_rows = self.session.get_torrent_names(client)
            top_item.create_children(client_rows)
        return

    def display_info(self):
        selected = self.currentItem()
        if selected.top: return
        t_hash = selected.t_hash
        client = selected.client
        db_rows = self.session.get_data_rows(t_hash,client)
        values = self.session.get_static_rows(t_hash,client)
        self.static.itemModel.receive_static(values)
        self.table.itemModel.receive_table(db_rows)
        self.compile_charts(db_rows)

    def compile_charts(self,db_rows):
        factory = self.session.factory
        ul,ratio,line = factory.compile_torrent_charts(db_rows)
        self.window.torrent_charts(ul,ratio,line)

    def sort_top_items(self,field):
        for num in range(self.topLevelItemCount()):
            item = self.topLevelItem(num)
            item.sort_children(field)
        return

    def get_top_items(self):
        for i in range(self.topLevelItemCount()):
            yield self.topLevelItem(i)

    def filter_active(self,active_hashes,x):
        for top_item in self.get_top_items():
            for i,item in top_item.get_children():
                if item.t_hash not in active_hashes: continue
                item.setHidden(x)
        return

class ChildTreeItem(QTreeWidgetItem):
    def __init__(self,item_type,row,session):
        super().__init__(item_type)
        self.setFont(0,Dubai())
        self.session = session
        self.label = row["name"]
        self.t_hash = row["hash"]
        self.client = row["client"]
        self.top = False
        self.setText(0,self.label)


class TopTreeItem(QTreeWidgetItem):
    def __init__(self,typ,client,session):
        super().__init__(typ)
        self.setFont(0,Cambria())
        self.top = True
        self.session = session
        self.client = client
        self.setText(0,self.client)

    def create_children(self,rows):
        for i,row in enumerate(rows):
            child = ChildTreeItem(0,row,self.session)
            self.addChild(child)
        return

    def get_children(self):
        for i in range(self.childCount()):
            yield (i,self.child(i))

    def sort_children(self,field):
        track = self.session.get_top_rows(self.client,field)
        counts = list(range(self.childCount()))[::-1]
        children = [self.takeChild(i) for i in counts]
        sort_children = sorted(children,key=lambda x: track[x.t_hash])
        [self.addChild(i) for i in sort_children]
        return
