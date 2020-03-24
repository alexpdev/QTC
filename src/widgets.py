#!/usr/bin/python
#! -*- coding: utf-8 -*-

################################################################################
######
###
## QTorrentCompanion v0.2
##
## This code written for the "QTorrentCompanion" program
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

from PyQt5.QtGui import QFont, QStandardItemModel, QStandardItem

from PyQt5.QtWidgets import (QTreeWidget, QTreeWidgetItem, QTableView,
                             QFrame, QMenuBar, QMenu, QAction)

from PyQt5.QtCore import Qt

from src.factory import ItemFactory


class SomeKindOfError(Exception):
    pass


class MenuBar(QMenuBar):
    def __init__(self,parent=None):
        super().__init__(parent=parent)
        self.window = parent
        self.setObjectName(u"menubar")
        font = SansFont()
        font.setPointSize(11)
        font.setBold(True)
        self.setFont(font)
        self.setStyleSheet("""
            MenuBar {
                background: #000;
                color: #0cc;
                border-bottom: 1px solid #0ff;
                }
            QMenu::item:selected {
                background-color: #aaa;
            }""")

    def add_menus(self):
        self.window.add_file_menu()
        self.columnsMenu = QMenu("Columns",parent=self)
        self.addMenu(self.columnsMenu)
        for field in self.dataTable.get_columns():
            action = QAction(field,parent=self.window)
            action.setCheckable(True)
            func = lambda checked,x=field: self.toggle_column(x,checked)
            self.columnsMenu.addAction(action)
            action.triggered.connect(func)
        return

    def assign(self,session,staticTable,dataTable,win):
        self.session = session
        self.staticTable = staticTable
        self.dataTable = dataTable
        self.window = win
        self.add_menus()

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


class TableView(QTableView):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.window = parent
        self.setShowGrid(True)
        self.setStyleSheet("background: #ddd; border: 1px solid #700; gridline-color: #79a392; color: #000;")
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

    def setSession(self,session):
        self.session = session
        self.row_map = session.static_fields
        self.col_map = session.data_fields
        return

    def receive_static(self,data):
        self.isEmpty()
        row = data[0]
        self.setColumnCount(2)
        self.setRowCount(len(row))
        for field in self.row_map:
            label,item = self.session.gen_items(field,row[field])
            self.setItem(self.row_count,0,label)
            self.setItem(self.row_count,1,item)
            self.row_count += 1
        self.view.resizeColumnsToContents()
        return

    def receive_table(self,data):
        self.isEmpty()
        first = data[0]
        self.setColumnCount(len(first))
        self.setRowCount(len(data))
        headers = []
        for x,row in enumerate(data):
            for y,field in enumerate(self.col_map):
                label,item = self.session.gen_items(field,row[field])
                if x == 0:
                    self.setHorizontalHeaderItem(y,label)
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
        self.parent = parent
        self.css = "background: #ccc; color: #022; border: 2px solid #600;"
        self.setStyleSheet(self.css)
        self.fancyfont = FancyFont()
        self.sansfont = SansFont()
        self.sansfont.setPointSize(10)
        self.fancyfont.setPointSize(11)
        self.fancyfont.setBold(True)
        self.setFrameShadow(QFrame.Sunken)
        self.setAlternatingRowColors(True)
        self.setAnimated(True)
        self.setUniformRowHeights(True)
        self.setHeaderHidden(True)
        self.setIndentation(4)
        self.setFont(self.fancyfont)
        self.setColumnCount(1)

    def add_items(self):
        for client in self.session.get_client_names():
            top_item = TreeItem.createTop(0,client)
            self.addTopLevelItem(top_item)
            for vals in self.session.get_torrent_names(client):
                tree_item = TreeItem.create(0,*vals)
                tree_item.setFont(0,self.fancyfont)
                top_item.addChild(tree_item)
        self.itemSelectionChanged.connect(self.display_info)

    def assign(self,session=None,static=None,table=None):
        self.session = session
        self.table = table
        self.static = static
        self.add_items()
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


class TreeItem(QTreeWidgetItem):
    def __init__(self,typ):
        super().__init__(typ)
        self.typ = typ
        self.top = False

    @classmethod
    def create(cls,typ,name,t_hash,client):
        item = cls(typ)
        item.label = name
        item.t_hash = t_hash
        item.client = client
        item.setText(0,name)
        return item

    @classmethod
    def createTop(cls,typ,client):
        item = cls(typ)
        item.client = client
        item.top = True
        item.setText(0,client)
        return item


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
