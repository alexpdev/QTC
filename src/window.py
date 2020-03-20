#!/usr/bin/python
#! -*- coding: utf-8 -*-

################################################################################
######
###
## Qbt Companion v0.1
##
## This code written for the "Qbt Companion" program
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
### PARTY HAS BEEN ADVISED OF THE POSSIBILITY OF SUCH DAMAGES.
######
################################################################################

import sys

from PyQt5.QtCore import (QCoreApplication, QMetaObject,
                          QObject, QPoint, QRect, QSize, Qt, QUrl)

from PyQt5.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
                         QFont,QFontDatabase, QIcon, QLinearGradient,
                         QPainter, QPalette, QPixmap, QRadialGradient)

from PyQt5.QtWidgets import (QApplication, QFrame, QGridLayout, QHBoxLayout,
                             QLabel, QListView, QListWidget, QListWidgetItem,
                             QMainWindow, QMenu, QMenuBar, QOpenGLWidget,
                             QPushButton, QStatusBar, QTableWidget,
                             QGraphicsWidget, QTableWidgetItem, QTabWidget,
                             QVBoxLayout, QWidget)

from src.widgets import (ComboBox, FancyFont, ListItem, TreeWidget,
                         TorrentNames, ListWidget, SansFont, StaticButton)


class Win(QMainWindow):

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.session = None
        self.setup_ui()


    def setup_ui(self):
        self.setWindowTitle("Torrent Companion")
        self.resize(1400, 800)
        self.setStyleSheet("background : #555; color: #fff;")

        # Central Widget and Layout
        self.gridLayoutWidget = QWidget()
        self.gridLayoutWidget.setObjectName(u"gridLayoutWidget")

        # List Widgets
        self.static = ListWidget(parent=self.gridLayoutWidget)
        self.static.setObjectName(u"static_torrent_data")

        self.tree = TreeWidget(parent=self.gridLayoutWidget)
        self.tree.setObjectName("Names")

        self.horizontalLayout = QHBoxLayout(self.gridLayoutWidget)
        self.horizontalLayout.setSpacing(2)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.horizontalLayout.setContentsMargins(5,5,5,5)
        self.horizontalLayout.addWidget(self.tree)


        # self.gridLayout = QGridLayout(self.gridLayoutWidget)
        # self.gridLayout.setObjectName(u"gridLayout")
        # self.gridLayout.setContentsMargins(10, 10, 10, 10)
        # self.torrentNames = TorrentNames(parent=self.gridLayoutWidget)
        # self.torrentNames.setObjectName(u"Names")
        # self.torrentNames.setObjectName("Names")

        # Combo Box
        # self.combo = ComboBox(self.gridLayoutWidget)
        # self.combo.setObjectName(u"comboBox")
        # self.combo.setEditable(False)
        # self.btn1 = StaticButton("Select",self.gridLayoutWidget)
        # self.btn1.setObjectName(u"staticButton")

        # self.gridLayout.addWidget(self.torrentNames, 2, 0, -1, 1)
        # self.gridLayout.addWidget(self.static, 0, 1, 4, -1)
        # self.gridLayout.addWidget(self.combo, 0, 0, 1, 1)
        # self.gridLayout.addWidget(self.btn1, 1, 0, 1, 1)

        # self.tabWidget = QTabWidget()
        # self.tabWidget.setObjectName(u"tabWidget")
        # self.tab = QWidget()
        # self.tab.setObjectName(u"tab")

        # self.verticalLayout2 = QVBoxLayout()
        # self.verticalLayout2.setSpacing(2)
        # self.verticalLayout2.setObjectName(u"verticalLayout2")
        # self.verticalLayout2.setContentsMargins(5, 5, 5, 5)
        # self.verticalLayout2.addWidget(self.static)

        # self.gridLayout.addLayout(self.verticalLayout,5,1,-1,-1)
        # self.tab.setLayout(self.verticalLayout)
        # self.tabWidget.addTab(self.tab, "DataTable")

        # self.tab_2 = QWidget()
        # self.tab_2.setObjectName(u"tab_2")
        # self.tabWidget.addTab(self.tab_2, "Graphs")
        # self.verticalLayout2.addLayout(self.verticalLayout)

        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setSpacing(2)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(5, 5, 5, 5)

        self.table_data = QTableWidget(self.gridLayoutWidget)
        self.table_data.setObjectName(u"tableWidget")
        self.table_data.setStyleSheet( """color : #000; background : #e6e6e6;
                                            border : 2px solid #000;""")
        self.table_data.setFrameShape(QFrame.WinPanel)
        self.table_data.setFrameShadow(QFrame.Sunken)
        self.verticalLayout.addWidget(self.static)
        self.verticalLayout.addWidget(self.table_data)
        self.horizontalLayout.addLayout(self.verticalLayout)
        self.horizontalLayout.setStretch(1,5)

        # self.gridLayout.setRowStretch(2, 2)
        # self.gridLayout.setRowStretch(1, 2)
        # self.gridLayout.setRowStretch(5, 4)
        # self.gridLayout.setColumnStretch(0, 1)
        # self.gridLayout.setColumnStretch(1, 4)

        self.setCentralWidget(self.gridLayoutWidget)

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
        # self.tabWidget.setCurrentIndex(0)
        QMetaObject.connectSlotsByName(self)


    def print_something(self):
        print("I have been clicked")

    def destroy_something(self):
        self.destroy()
        sys.exit(self.exec_())

    def assign_session(self,session):
        self.session = session
        # self.combo.assign(self.session)
        # self.btn1.assign(self.combo,self.session,self.torrentNames)
        # self.torrentNames.assign(self.session,self.static,self.table_data)
        self.tree.assign(self.session,self.static,self.table_data)
