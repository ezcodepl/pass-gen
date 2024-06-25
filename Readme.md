**Installation**
In a virtual environment, install by issuing the command:

pip install --upgrade cx_Freeze

To install the latest development build:

pip install --force --no-cache --pre --extra-index-url https://marcelotduarte.github.io/packages/ cx_Freeze

**Python requirements
Python requirements are installed automatically by pip, pipenv, or conda.**

setuptools >= 62.6
typing_extensions >= 4.10.0 (Python 3.8, 3.9)
wheel >= 0.42.0
cx_Logging >= 3.1           (Windows only)
lief >= 0.12.0              (Windows only)
filelock >=3.11.0           (Linux)
patchelf >= 0.14            (Linux)
C compiler                  (required only if installing from sources)



**In setup.py select file name generator_v*.py  (select version app)**
                             
**Make buil.exe file from generator_v*.py**
                             
python setup.py build

**Copy folder build on own folder on disk and run file generator.exe**
