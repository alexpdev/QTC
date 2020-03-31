from PyQt5.QtGui import QFont

class _CustomFont(QFont):
    def __init__(self):
        super().__init__()
        self.assign()

    def assign(self):
        self.setFamily(self.info["name"])
        self.setPointSize(self.info["size"])
        self.setBold(self.info["bold"])


class Cambria(_CustomFont):
    info = {"name":"Cambria","size":11,"bold":False}
    def __init__(self):
        super().__init__()

class Niagara(_CustomFont):
    info = {"name":"Niagara","size":9,"bold":False}
    def __init__(self):
        super().__init__()


class Dubai(_CustomFont):
    info = {"name":"Dubai","size":8, "bold":False}
    def __init__(self):
        super().__init__()
