from PyQt5.QtWidgets import QMenubar, QMenu, QAction


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
