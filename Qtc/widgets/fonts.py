from PyQt5.QtGui import QFont

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
