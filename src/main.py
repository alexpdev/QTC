import os
import sys
from time import sleep
from pathlib import Path
from PyQt5.QtWidgets import QApplication

path = Path(__file__).resolve()
ROOT = path.parent.parent
sys.path.append(str(ROOT))

from settings import items
from src.session import Session,SessionManager
from src.window import Win

def main(k,v):
    session = Session(name=k,**v)
    a = session.login()
    b = session.get_info()
    session.log(b)
    return session

if __name__ == "__main__":
    app = QApplication(sys.argv)
    man = SessionManager()
    for k,v in items.items():
        session = main(k,v)
        man.add_session(session)
    win = Win()
    man.set_window(win)
    win.set_tree_data(man)
    win.show()
    sys.exit(app.exec_())
