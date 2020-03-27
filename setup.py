from setuptools import setup, find_packages
import os,sys
from pathlib import Path
from QTorrentCompanion.version import __version__ as version

here = os.path.abspath(os.path.dirname(__file__))
requirements = open("requirements.txt","rt").read().split("\n")
README = open(os.path.join(here, 'README.md')).read()
start_script = Path(here) / "bin" / "QTC_v0.2.py"

setup(
    name="QBittorrentCompanion",
    version=version,
    packages=find_packages(),
    author="AlexPdev",
    author_email="alexpdev@protonmail.com",
    description="GUI application for viewing torrent stats.",
    keywords=["torrents"],
    url="https://github.com/alexpdev/QTorrentCompanion",
    license='AGPLv3.0',
    install_requires=requirements,
    zip_safe=False,
    include_package_data=True,
    python_requires="~=3.*",
)
