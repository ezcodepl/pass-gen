import sys

from cx_Freeze import setup, Executable

# Opcje konfiguracyjne
build_exe_options = {
    "packages": ["tkinter", "random", "string", "csv", "pandas"],
    "include_files": []
}

# Skrypt do wykonania
base = None

# Ustawienie dla Windows
if sys.platform == "win32":
    base = "Win32GUI"

setup(
    name = "Generator Haseł",
    version = "1.0",
    description = "Prosty generator haseł",
    options = {"build_exe": build_exe_options},
    executables = [Executable("generator_v3.py", base=base)]
)
