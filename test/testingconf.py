import sys
import os
from pathlib import Path
from dotenv import load_dotenv
load_dotenv()
BASE_DIR = os.environ["BASE_DIR"]
sys.path.append(BASE_DIR)
