from setuptools import setup, find_packages
import os,sys
from pathlib import Path
from Qtc.version import __version__ as version

here = os.path.abspath(os.path.dirname(__file__))
requirements = ["PyQt5", "PyQt5-sip","requests","urllib3","PyQtChart"]
README = open(os.path.join(here, 'README.md')).read()
start_script = Path(here) / "bin" / "Qtc_v0.2.py"

setup(
    name="Qtcomp",
    version=version,
    packages=find_packages(),
    author="AlexPdev",
    author_email="alexpdev@protonmail.com",
    description="GUI application for viewing torrent stats.",
    keywords=["torrents"],
    url="https://github.com/alexpdev/Qtc",
    license='AGPLv3.0',
    install_requires=requirements,
    zip_safe=False,
    entry_points={'console_scripts':['Qtc=Qtc.bin.Qtc_:main']},
    include_package_data=True,
    python_requires="~=3.*",
)
