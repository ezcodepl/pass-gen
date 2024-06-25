# Pass Gen

A simple password generator with the ability to save generated password lists to .txt, .csv, .xlsx formats. 

The program allows you to generate a password from min. 8 characters, above 20 characters passwords are very strong. The generated passwords contain at least: 2 digits, lowercase and uppercase letters and min. 2 special characters.

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



**In setup.py select file name generator_v.py  (select version app)**
                             
**Make buil.exe file from generator_v.py**
                             
python setup.py build

**Copy folder build to own folder on disk and run file generator.exe**


# [PL]

Prosty generator haseł z możliwością zapisywania wygenerowanych list haseł do formatów .txt, .csv, .xlsx.

Program umożliwia wygenerowanie hasła już od min. Hasła składające się z 8 znaków i powyżej 20 znaków są bardzo silne. Wygenerowane hasła zawierają co najmniej: 2 cyfry, małe i duże litery oraz min. 2 znaki specjalne.

**Instalacja W środowisku wirtualnym zainstaluj wydając polecenie:**

pip install --upgrade cx_Freeze

**Aby zainstalować najnowszą wersję rozwojową:**

pip install --force --no-cache --pre --extra-index-url https://marcelotduarte.github.io/packages/ cx_Freeze

**Wymagania Pythona Wymagania Pythona są instalowane automatycznie przez pip, pipenv lub conda.**

setuptools >= 62.6 typing_extensions >= 4.10.0 (Python 3.8, 3.9) Wheel >= 0.42.0 cx_Logging >= 3.1 (tylko Windows) Lief >= 0.12.0 (tylko Windows) filelock >=3.11.0 (Linux) patchelf >= 0.14 (Linux) Kompilator C (wymagany tylko w przypadku instalacji ze źródeł)

**W setup.py wybierz nazwę pliku generator_v.py (wybierz wersję aplikacji)**

**Utwórz plik build.exe z generator_v.py**

python setup.py build

**Skopiuj folder kompilacji do własnego folderu na dysku i uruchom plik generator.exe**
