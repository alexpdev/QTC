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

from PyQt5.QtWidgets import QTreeWidget, QTreeWidgetItem, QTableView

from PyQt5.QtCore import Qt

from src.factory import ItemFactory


class TableView(QTableView):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.parent = None
        self.setShowGrid(True)
        self.setStyleSheet("background: #ddd; border: 1px solid #700; gridline-color: #79a392; color: #000;")

    def assign(self,session):
        self.session = session
        self.manager = ItemModel(parent=self)
        self.setModel(self.manager)


class ItemModel(QStandardItemModel):
    def __init__(self,parent=None):
        super().__init__(parent=None)
        self.view = parent
        self.row_count = 0
        self.factory = ItemFactory()
        self.flags = (Qt.ItemIsSelectable|Qt.ItemIsEnabled)

    def receive_static(self,data):
        self.isEmpty()
        row = data[0]
        self.setColumnCount(2)
        self.setRowCount(len(row))
        for k,v in zip(row.keys(),tuple(row)):
            label,item = self.factory.gen_item(k,v)
            self.setItem(self.row_count,0,label)
            self.setItem(self.row_count,1,item)
            self.row_count += 1
        self.view.resizeColumnsToContents()

    def receive_table(self,data):
        self.isEmpty()
        first = data[0]
        keys = list(first.keys())
        self.setColumnCount(len(first))
        self.setRowCount(len(data))
        for x,row in enumerate(data):
            for y,vals in enumerate(tuple(row)):
                field,val = self.factory.gen_item(keys[y],vals)
                if x == 0:
                    self.setHorizontalHeaderItem(y,field)
                self.setItem(x,y,val)
            self.row_count += 1

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
        self.fancyfont.setPointSize(9)
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
    info = {"name":"Leelawadee","size":9,"bold":False}
    def __init__(self):
        super().__init__()


class SansFont(CustomFont):
    info = {"name":"Dubai Medium","size":9,"bold":True}
    def __init__(self):
        super().__init__()
