import os
import sys
from pathlib import Path
from unittest import TestCase
BASE_DIR = Path(os.path.abspath(__file__)).parent.parent
sys.path.append(BASE_DIR)
from dotenv import load_dotenv

load_dotenv()

from test.testsettings import DETAILS,DB_NAME,DATA_DIR
from src.mixins import RequestMixin, QueryMixin


