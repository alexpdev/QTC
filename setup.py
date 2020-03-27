from setuptools import setup, find_packages
import os,sys


with open('README.md') as readme_file:
    readme = readme_file.read()

with open('HISTORY.md') as history_file:
    history = history_file.read()

requirements = ["PyQt5", "PyQt5-sip","requests","urllib3","PyQtChart"]
setup(
    author="AlexpDev",
    author_email='alexpdev@protonmail.com',
    python_requires='>=3.5',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    entry_points={'console_scripts':['Qtc=Qtc.bin.Qtc_:main']},
    description="GUI tool for viewing torrent stats.",
    install_requires=requirements,
    long_description=readme + '\n\n' + history,
    include_package_data=True,
    keywords='qtc',
    name='Qtc',
    packages=find_packages(include=['Qtc', 'Qtc.*']),
    test_suite='test',
    url='https://github.com/alexpdev/qtc',
    version='0.2',
    zip_safe=False,
    license='AGPLv3.0',
)
