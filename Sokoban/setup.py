import cx_Freeze 

exe = [cx_Freeze.Executable("Sokoban.py")]

cx_Freeze.setup( name = "downloads", version = "1.0", options = {"build_exe": {"packages": ["errno", "os", "re", "stat", "subprocess","collections", "pprint","shutil", "humanize","pycallgraph"], "include_files": []}}, executables = exe ) 