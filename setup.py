import sys
from cx_Freeze import setup, Executable

# Dependencies are automatically detected, but it might need fine tuning.
build_exe_options = {"packages": ["os"
,"asks"
,"asyncio"
,"certifi"
,"chardet"
,"curio"
,"Django"
,"get"
,"h11"
,"idna"
,"multidict"
,"post"
,"public"
,"pygame"
,"pytz"
,"requests"
,"setupfiles"
,"urllib3"
,"yarl"], "excludes": ["tkinter"],"include_files":["background","sprite","sound"]}

# GUI applications require a different base on Windows (the default is for a
# console application).
base = None
if sys.platform == "win32":
    base = "Win32GUI"

setup(  name = "MedievalBrawler",
        version = "0.1",
        description = "MedievalBrawler",
        options = {"build_exe": build_exe_options},
        executables = [Executable("__init__.py", base=base)])