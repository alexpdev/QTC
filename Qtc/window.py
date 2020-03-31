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

import sys
from PyQt5.QtCore import QSize, Qt, QMetaObject
from PyQt5.QtGui import QPainter
from PyQt5.QtWidgets import (QApplication, QHBoxLayout, QMenu,
                             QMenuBar, QStatusBar, QMainWindow,
                             QVBoxLayout, QWidget, QSplitter,
                             QTabWidget, QAction, QGraphicsWidget)

from PyQt5.QtChart import QChart, QChartView, QScatterSeries

from qtc.widgets.treeview import ChildTreeItem, TopTreeItem, TreeWidget
from qtc.widgets.tables import ItemModel, StandardItem, TableView
from qtc.widgets.menubar import MenuBar
from qtc.widgets.fonts import Cambria, Niagara, Dubai

class Win(QMainWindow):

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setup_ui()

    def setup_ui(self):
        self.setWindowTitle("Torrent Companion")
        self.resize(1400, 800)
        self.hSplitter = QSplitter()
        self.tree = TreeWidget(parent=self.hSplitter)
        self.hSplitter.addWidget(self.tree)
        self.tables = QWidget(self.hSplitter)
        self.hLayout = QHBoxLayout(self.tables)
        self.tables.setLayout(self.hLayout)
        self.hSplitter.addWidget(self.tables)
        self.vSplitter = QSplitter(parent=self.tables)
        self.vSplitter.setOrientation(Qt.Vertical)
        self.hLayout.addWidget(self.vSplitter)
        self.staticTable = TableView(self.vSplitter)
        self.vSplitter.addWidget(self.staticTable)
        self.tabs = QTabWidget(parent=self.vSplitter)
        self.dataTable = TableView(self.tabs)
        self.tabs.addTab(self.dataTable,"data")
        self.hSplitter.setStretchFactor(1,4)
        self.vSplitter.addWidget(self.tabs)
        self.vSplitter.setStretchFactor(1,3)
        self.add_chart_tabs()
        self.setCentralWidget(self.hSplitter)
        self.menubar = MenuBar(parent=self)
        self.setMenuBar(self.menubar)
        statusbar = self.statusBar()
        statusbar.setObjectName(u"statusbar")
        QMetaObject.connectSlotsByName(self)

    def add_chart_tabs(self):
        self.ulChart = QChartView(parent=self.tabs)
        self.ratioChart = QChartView(parent=self.tabs)
        self.lineChart = QChartView(parent=self.tabs)
        self.ulChart.setRenderHint(QPainter.Antialiasing)
        self.ratioChart.setRenderHint(QPainter.Antialiasing)
        self.lineChart.setRenderHint(QPainter.Antialiasing)
        self.tabs.addTab(self.lineChart,"Line Chart")
        self.tabs.addTab(self.ratioChart,"Ratio Chart")
        self.tabs.addTab(self.ulChart,"Uploaded Chart")
        return

    def torrent_charts(self,upload_chart,ratio_chart,line_chart):
        self.ulChart.setChart(upload_chart)
        self.ratioChart.setChart(ratio_chart)
        self.lineChart.setChart(line_chart)
        return

    def open_settings(self):
        pass

    def exit_window(self):
        self.destroy()
        self.session.end_session()

    def assign_session(self,session):
        self.session = session
        self.staticTable.assign(session,self)
        self.dataTable.assign(session,self)
        self.tree.assign(session,self)
        self.menubar.assign(session,self)
