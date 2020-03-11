#! /bin/python3
"""






    Just in case














"""

import sys
import os
from pathlib import Path
from dotenv import load_dotenv as lde
BASE_DIR = Path(".").resolve().parent
sys.path.append(BASE_DIR)
from src.db import QDB

lde()

DEBUG = False




