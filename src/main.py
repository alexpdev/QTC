import os
import sys
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
    # a = session.login()
    # b = session.get_info()
    # session.log(b)
    return session

if __name__ == "__main__":
    app = QApplication(sys.argv)
    man = SessionManager()
    for k,v in items.items():
        session = main(k,v)
        man.add_session(session)
    win = Win()
    win.set_session_manager(man)
    win.show()
    sys.exit(app.exec_())
