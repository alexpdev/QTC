import sys
import os
import json
import string
from datetime import datetime
from PyQt5.QtWidgets import      (   QLabel,
                                     QFrame,
                                    QWidget,
                                   QMenuBar,
                                  QComboBox,
                                  QDateEdit,
                                 QStatusBar,
                                QMainWindow,
                                QListWidget,
                                QVBoxLayout,
                                QHBoxLayout,
                                QGridLayout,
                                QPushButton,
                                QTreeWidget,
                               QTableWidget,
                               QApplication,
                            QTreeWidgetItem,
)
from PyQt5.QtGui import QFont

class Win(QMainWindow):

    def __init__(self,master=None):
        super().__init__(master)
        self.master = master
        self.setWindowTitle("Torrent Companion")
        self.resize(900,700)
        centralWidget = QWidget(self)
        font = QFont()
        font.setPointSize(12)
        font.setBold(False)
        centralWidget.setFont(font)
        centralWidget.resize(870,650)
        self.session_combo = QComboBox(centralWidget)
        self.statusBar = QStatusBar(centralWidget)
        self.startDate = QDateEdit(centralWidget)
        slabel = QLabel("Start Date")
        elabel = QLabel("End Date")
        self.endDate = QDateEdit(centralWidget)
        self.menuBar = QMenuBar(centralWidget)
        self.btn1 = QPushButton("Load Info",centralWidget)
        self.tree = QTreeWidget(centralWidget)
        self.list = QListWidget(centralWidget)
        grid = QGridLayout(centralWidget)
        grid.addWidget(self.btn1,0,0)
        grid.addWidget(slabel,0,1)
        grid.addWidget(self.startDate,0,2)
        grid.addWidget(elabel,0,3)
        grid.addWidget(self.endDate,0,4)
        grid.addWidget(self.tree,1,0)
        grid.addWidget(self.list,1,1,1,4)
        grid.setHorizontalSpacing(10)
        grid.setVerticalSpacing(10)
        for i in range(5):
            grid.setColumnStretch(i,1)
        self.setCentralWidget(centralWidget)
        centralWidget.setLayout(grid)

    def set_tree_data(self,man):
        for session in man.sessions:
            tree_item = QTreeWidgetItem(self.tree)
            tree_item.setText(0,session.name)
            self.set_tree_children(tree_item,session)
            self.tree.addTopLevelItem(tree_item)

    def set_tree_children(self,tree_item,session):
        lst = []
        for model in session.load_models():
            if model.hash in lst: continue
            titem = QTreeWidgetItem(parent=tree_item)
            titem.setText(1,model.name)
            titem.model = model
            lst.append(model.hash)
        return

app = QApplication(sys.argv)
win = Win()
sys.exit(app.exec_())





"""
        Window->resize(788, 600);
        centralwidget = new QWidget(Window);
        centralwidget->setObjectName(QStringLiteral("centralwidget"));
        widget = new QWidget(centralwidget);
        widget->setObjectName(QStringLiteral("widget"));
        widget->setGeometry(QRect(20, 10, 761, 531));
        verticalLayoutWidget = new QWidget(widget);
        verticalLayoutWidget->setObjectName(QStringLiteral("verticalLayoutWidget"));
        verticalLayoutWidget->setGeometry(QRect(0, -1, 751, 531));
        verticalLayout = new QVBoxLayout(verticalLayoutWidget);
        verticalLayout->setObjectName(QStringLiteral("verticalLayout"));
        verticalLayout->setContentsMargins(0, 0, 0, 0);
        horizontalLayout = new QHBoxLayout();
        horizontalLayout->setObjectName(QStringLiteral("horizontalLayout"));
        pushButton = new QPushButton(verticalLayoutWidget);
        pushButton->setObjectName(QStringLiteral("pushButton"));

        horizontalLayout->addWidget(pushButton);

        label = new QLabel(verticalLayoutWidget);
        label->setObjectName(QStringLiteral("label"));

        horizontalLayout->addWidget(label);

        dateEdit = new QDateEdit(verticalLayoutWidget);
        dateEdit->setObjectName(QStringLiteral("dateEdit"));

        horizontalLayout->addWidget(dateEdit);

        label_2 = new QLabel(verticalLayoutWidget);
        label_2->setObjectName(QStringLiteral("label_2"));

        horizontalLayout->addWidget(label_2);

        dateEdit_2 = new QDateEdit(verticalLayoutWidget);
        dateEdit_2->setObjectName(QStringLiteral("dateEdit_2"));

        horizontalLayout->addWidget(dateEdit_2);


        verticalLayout->addLayout(horizontalLayout);

        horizontalLayout_2 = new QHBoxLayout();
        horizontalLayout_2->setObjectName(QStringLiteral("horizontalLayout_2"));
        treeWidget = new QTreeWidget(verticalLayoutWidget);
        QTreeWidgetItem *__qtreewidgetitem = new QTreeWidgetItem();
        __qtreewidgetitem->setText(0, QStringLiteral("1"));
        treeWidget->setHeaderItem(__qtreewidgetitem);
        treeWidget->setObjectName(QStringLiteral("treeWidget"));

        horizontalLayout_2->addWidget(treeWidget);

        listView = new QListView(verticalLayoutWidget);
        listView->setObjectName(QStringLiteral("listView"));

        horizontalLayout_2->addWidget(listView);

        horizontalLayout_2->setStretch(0, 1);
        horizontalLayout_2->setStretch(1, 3);

        verticalLayout->addLayout(horizontalLayout_2);

        Window->setCentralWidget(centralwidget);
        menubar = new QMenuBar(Window);
        menubar->setObjectName(QStringLiteral("menubar"));
        menubar->setGeometry(QRect(0, 0, 788, 21));
        menubar->setDefaultUp(true);
        Window->setMenuBar(menubar);
        statusbar = new QStatusBar(Window);
        statusbar->setObjectName(QStringLiteral("statusbar"));
        Window->setStatusBar(statusbar);
#ifndef QT_NO_SHORTCUT
        label->setBuddy(dateEdit);
        label_2->setBuddy(dateEdit_2);
#endif // QT_NO_SHORTCUT

        retranslateUi(Window);

        QMetaObject::connectSlotsByName(Window);
    } // setupUi
"""
