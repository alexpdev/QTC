from PyQt5.QtWidgets import QMenuBar, QMenu, QAction

class MenuBar(QMenuBar):
    def __init__(self,parent=None):
        super().__init__(parent=parent)
        self.setObjectName(u"menubar")
        self.window = parent

    def assign(self,session,window):
        self.session = session
        self.window = window
        self.staticTable = window.staticTable
        self.dataTable = window.dataTable
        self.tree = window.tree
        self.active_hashes = self.session.get_active_hashes()
        self.add_menus()

    def add_menus(self):
        self.add_file_menu()
        self.add_filters_menu()
        self.add_columns_menu()
        self.add_sort_menu()

    def add_file_menu(self):
        self.file_menu = QMenu("File",parent=self)
        self.addMenu(self.file_menu)
        exit_action = QAction("Exit",parent=self.window)
        settings = QAction("Settings",parent=self.window)
        self.file_menu.addAction(exit_action)
        self.file_menu.addAction(settings)
        exit_action.triggered.connect(self.window.exit_window)
        settings.triggered.connect(self.open_settings)
        return

    def add_columns_menu(self):
        self.columnsMenu = QMenu("Columns",parent=self)
        self.addMenu(self.columnsMenu)
        for field in self.dataTable.get_columns():
            action = QAction(field,parent=self.window)
            action.setCheckable(True)
            self.columnsMenu.addAction(action)
            func = lambda checked,x=field: self.toggle_column(x,checked)
            action.triggered.connect(func)
        return

    def add_filters_menu(self):
        self.view_menu = QMenu("View",parent=self)
        self.addMenu(self.view_menu)
        self.filter_menu = QMenu("Filters",parent=self)
        self.view_menu.addMenu(self.filter_menu)
        filterActive = QAction("Active Only",parent=self.window)
        filterActive.setCheckable(True)
        func = lambda x: self.filter_active_torrents(x)
        filterActive.triggered.connect(func)
        self.filter_menu.addAction(filterActive)
        return

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
        return

    def sort_tree(self,x,field):
        self.tree.sort_top_items(field)
        return


    def filter_active_torrents(self,x=True):
        self.tree.filter_active(self.active_hashes,x)
        return

    def open_settings(self):
        self.window.open_settings()

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
