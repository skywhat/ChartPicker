from distutils.core import setup
import py2exe
import sys

# this allows to run it with a simple double click.
sys.argv.append('py2exe')

py2exe_options = {
    "includes": ["matplotlib","numpy","mpldatacursor","wx","data_csv"],
    "dll_excludes": ["MSVCP90.dll", ],
    "compressed": 1,
    "optimize": 2,
    "ascii": 0,
}

setup(
    name='Sync',
    version='1.0',
    windows=[{"script": 'ChartPickerGUI.py'}],
    zipfile=None,
    options={'py2exe': py2exe_options}
)