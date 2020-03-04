import os,sys
__getpath__ = lambda x: os.path.abspath(os.path.dirname(os.path.abspath(x)))


ROOT = __getpath__(__file__)
os.path.append(ROOT)
