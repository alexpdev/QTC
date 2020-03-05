import sys
from pathlib import Path

path = Path(__file__).resolve()
ROOT = path.parent.parent
sys.path.append(str(ROOT))

from etc.conf import (DATA_DIRNAME,
                      FILEPREFIX,
                      FILESUFFIX)

import urls

URLs = urls

_vars = {
    "prefix" : FILEPREFIX,
    "suffix" : FILESUFFIX,
    "data" : ROOT / DATA_DIRNAME,
    "urls" : urls
}
