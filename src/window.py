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

import sys
from PyQt5.QtCore import QRect, QSize, Qt, QMetaObject
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import (QApplication, QHBoxLayout, QMenu,
                             QMenuBar, QStatusBar, QMainWindow,
                             QVBoxLayout, QWidget, QSplitter)

from src.widgets import FancyFont, TreeWidget, SansFont, TableView, ItemModel


class Win(QMainWindow):

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setup_ui()

    def setup_ui(self):
        self.setWindowTitle("Torrent Companion")
        self.resize(1400, 800)
        self.setStyleSheet("background : #444; color: #fff;")

        self.hSplitter = QSplitter()
        self.tree = TreeWidget(parent=self.hSplitter)
        self.tree.setObjectName("Names")
        self.hSplitter.addWidget(self.tree)
        self.tables = QWidget(self.hSplitter)
        self.hSplitter.addWidget(self.tables)
        self.hLayout = QHBoxLayout(self.tables)
        self.vSplitter = QSplitter(parent=self.tables)
        self.vSplitter.setOrientation(Qt.Vertical)
        self.hLayout.addWidget(self.vSplitter)
        self.dataTable = TableView(self.vSplitter)
        self.staticTable = TableView(self.vSplitter)
        self.vSplitter.addWidget(self.staticTable)
        self.vSplitter.addWidget(self.dataTable)
        self.setCentralWidget(self.hSplitter)

        menubar = self.menuBar()
        menufont = menubar.font()
        menufont.setPointSize(11)
        menubar.setFont(menufont)
        menubar.setObjectName(u"menubar")
        menubar.setStyleSheet("""background: #000; color: #0cc;
                              border-bottom: 1px solid #0ff;""")
        statusbar = self.statusBar()
        statusbar.setObjectName(u"statusbar")
        statusbar.setStyleSheet("""background: #000; color: #0ff;
                                border-bottom: 1px solid #0ff;""")
        self.file_menu = QMenu("File",parent=menubar)
        self.layout_menu = QMenu("Layout",parent=menubar)
        self.help_menu = QMenu("Help",parent=menubar)

        self.file_menu.addAction("Print",self.print_something)
        self.help_menu.addAction("Quit",self.destroy_something)

        menubar.addMenu(self.file_menu)
        menubar.addMenu(self.help_menu)
        QMetaObject.connectSlotsByName(self)

    def print_something(self):
        print("I have been clicked")

    def destroy_something(self):
        self.destroy()
        sys.exit(self.exec_())

    def assign_session(self,session):
        self.session = session
        self.staticTable.assign(self.session)
        self.dataTable.assign(self.session)
        self.tree.assign(self.session,self.staticTable,self.dataTable)
