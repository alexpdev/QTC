#!/usr/bin/python
#! -*- coding: utf-8 -*-

################################################################################
######
###
## Qtc v0.2
##
## This code written for the "Qtc" program
##
## This project is licensed with:
## GNU AFFERO GENERAL PUBLIC LICENSE
##
## Please refer to the LICENSE file locate in the root directory of this
## project or visit <https://www.gnu.org/licenses/agpl-3.0 for more
## information.
##
## THE COPYRIGHT HOLDERS PROVIDE THE PROGRAM "AS IS" WITHOUT WARRANTY OF ANY
## KIND, EITHER EXPRESSED OR IMPLIED, INCLUDING, BUT NOT LIMITED TO, THE
## IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE.
## THE ENTIRE RISK AS TO THE QUALITY AND PERFORMANCE OF THE PROGRAM IS WITH
## YOU. SHOULD THE PROGRAM PROVE DEFECTIVE, YOU ASSUME THE COST OF ALL
## NECESSARY SERVICING, REPAIR OR CORRECTION.
##
## IN NO EVENT ANY COPYRIGHT HOLDER, OR ANY OTHER PARTY WHO MODIFIES AND/OR
## CONVEYS THE PROGRAM AS PERMITTED ABOVE, BE LIABLE TO YOU FOR DAMAGES,
## INCLUDING ANY GENERAL, SPECIAL, INCIDENTAL OR CONSEQUENTIAL DAMAGES ARISING
## OUT OF THE USE OR INABILITY TO USE THE PROGRAM EVEN IF SUCH HOLDER OR OTHER
## PARTY HAS BEEN ADVISED OF THE POSSIBILITY OF SUCH DAMAGES.
###
######
################################################################################

import itertools

from PyQt5.QtGui import QFont, QStandardItemModel, QStandardItem, QPainter

from PyQt5.QtWidgets import (QTreeWidget, QTreeWidgetItem, QTableView,
                             QFrame, QMenuBar, QMenu, QAction)

from PyQt5.QtChart import QScatterSeries, QChart, QChartView, QLineSeries

from PyQt5.QtCore import Qt



class SomeKindOfError(Exception):
    pass


class MenuBar(QMenuBar):
    def __init__(self,parent=None):
        super().__init__(parent=parent)
        self.window = parent
        self.setObjectName(u"menubar")
        self.active_hashes = []
        self.tree_items = []

    def assign(self,session,staticTable,dataTable,win):
        self.session = session
        self.staticTable = staticTable
        self.dataTable = dataTable
        self.window = win
        self.add_menus()

    def add_menus(self):
        self.add_file_menu()
        self.add_filters_menu()
        self.add_columns_menu()
        self.add_sort_menu()

    def add_columns_menu(self):
        self.columnsMenu = QMenu("Columns",parent=self)
        self.addMenu(self.columnsMenu)
        for field in self.dataTable.get_columns():
            action = QAction(field,parent=self.window)
            action.setCheckable(True)
            func = lambda checked,x=field: self.toggle_column(x,checked)
            self.columnsMenu.addAction(action)
            action.triggered.connect(func)
        return

    def toggle_column(self,field,checked):
        columns = self.dataTable.get_columns()
        idx = columns.index(field)
        if checked:
            self.dataTable.checks.append((field,idx))
            self.dataTable.hideColumn(idx)
        else:
            self.dataTable.checks.remove((field,idx))
            self.dataTable.showColumn(idx)
        return

    def add_file_menu(self):
        self.file_menu = QMenu("File",parent=self)
        self.addMenu(self.file_menu)
        exit_action = QAction("Exit",parent=self.window)
        self.file_menu.addAction(exit_action)
        exit_action.triggered.connect(self.window.exit_window)


    def add_filters_menu(self):
        self.view_menu = QMenu("View",parent=self)
        self.addMenu(self.view_menu)
        self.filter_menu = QMenu("Filters",parent=self)
        self.view_menu.addMenu(self.filter_menu)
        filterActive = QAction("Active Only",parent=self.window)
        self.filter_menu.addAction(filterActive)
        filterActive.setCheckable(True)
        func = lambda x: self.filter_active_torrents(x)
        filterActive.triggered.connect(func)

    def add_sort_menu(self):
        self.sort_menu = QMenu("Sorting",parent=self)
        self.view_menu.addMenu(self.sort_menu)
        fields = ["uploaded","ratio","time_active","size"]
        for field in fields:
            action = QAction(field,parent=self.window)
            action.setCheckable(False)
            func = lambda x,field=field: self.sort_tree(x,field)
            self.sort_menu.addAction(action)
            action.triggered.connect(func)

    def sort_tree(self,x,field):
        self.window.tree.sort_top_items(field)


    def filter_active_torrents(self,x=True):
        if not x:
            if not self.active_hashes: return
            for item in self.tree_items:
                item.setHidden(False)
        elif not self.tree_items:
            self.active_hashes = self.session.get_active_hashes()
            for i in range(self.window.tree.topLevelItemCount()):
                item = self.window.tree.topLevelItem(i)
                for j in range(item.childCount()):
                    childItem = item.child(j)
                    if childItem.t_hash not in self.active_hashes:
                        childItem.setHidden(True)
                        self.tree_items.append(childItem)
        else:
            for item in self.tree_items:
                item.setHidden(True)

class TableView(QTableView):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.window = parent
        self.setShowGrid(True)
        self.checks = []

    def assign(self,session,window):
        self.window = window
        self.session = session
        self.manager = ItemModel(parent=self)
        self.manager.setSession(self.session)
        self.setModel(self.manager)
        return

    def get_columns(self):
        col = self.manager.col_map
        return col

    def get_rows(self):
        row = self.manager.row_map
        return row

    def check_menus(self):
        for field,idx in self.checks:
            self.hideColumn(idx)
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

class TreeWidget(QTreeWidget):
    def __init__(self,parent=None):
        super().__init__(parent=parent)
        self.setAlternatingRowColors(True)
        self.setAnimated(True)
        self.setStyleSheet("margin-top: 10px; margin-bottom: 10px;")
        self.setIndentation(18)
        self.setUniformRowHeights(True)
        self.setHeaderHidden(True)
        self.setColumnCount(1)

    def add_top_items(self):
        for client in self.session.get_client_names():
            top_item = TopTreeItem(0,client,self.session)
            self.addTopLevelItem(top_item)
            client_rows = self.session.get_torrent_names(client)
            top_item.create_children(client_rows)
        return

    def sort_top_items(self,field):
        for num in range(self.topLevelItemCount()):
            item = self.topLevelItem(num)
            item.sort_children(field)
        return

    def assign(self,session=None,static=None,table=None,window=None):
        self.session = session
        self.table = table
        self.static = static
        self.window = window
        self.add_top_items()
        self.itemSelectionChanged.connect(self.display_info)
        return

    def display_info(self):
        selected = self.currentItem()
        if selected.top: return
        t_hash = selected.t_hash
        client = selected.client
        db_rows = self.session.get_data_rows(t_hash,client)
        values = self.session.get_static_rows(t_hash,client)
        self.static.manager.receive_static(values)
        self.table.manager.receive_table(db_rows)
        self.compile_charts(db_rows)

    def compile_charts(self,db_rows):
        factory = self.session.factory
        ul,ratio,line = factory.compile_torrent_charts(db_rows)
        self.window.torrent_charts(ul,ratio,line)


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


class ChildTreeItem(QTreeWidgetItem):
    def __init__(self,item_type,row,session):
        super().__init__(item_type)
        self.session = session
        self.label = row["name"]
        self.t_hash = row["hash"]
        self.client = row["client"]
        self.top = False
        self.setText(0,self.label)

class TopTreeItem(QTreeWidgetItem):
    def __init__(self,typ,client,session):
        super().__init__(typ)
        self.top = True
        self.session = session
        self.client = client
        self.setText(0,self.client)

    def create_children(self,rows):
        for i,row in enumerate(rows):
            child = ChildTreeItem(0,row,self.session)
            self.addChild(child)
        return

    def sort_children(self,field):
        track = self.session.get_top_rows(self.client,field)
        counts = list(range(self.childCount()))[::-1]
        children = [self.takeChild(i) for i in counts]
        sort_children = sorted(children,key=lambda x: track[x.t_hash])
        [self.addChild(i) for i in sort_children]
        return

class _CustomFont(QFont):
    def __init__(self):
        super().__init__()
        self.assign()

    def assign(self):
        self.setFamily(self.info["name"])
        self.setPointSize(self.info["size"])
        self.setBold(self.info["bold"])


class FancyFont(_CustomFont):
    info = {"name":"Leelawadee","size":9,"bold":False}
    def __init__(self):
        super().__init__()


class SansFont(_CustomFont):
    info = {"name":"Dubai Medium","size":8, "bold":False}
    def __init__(self):
        super().__init__()
