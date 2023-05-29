# coding: utf-8
#        [dashedgeless] command file
# ------  Welcome to [dashedgeless]!  -------
# this program cannot run in GUI
# please use the 'dash' command to call it
# -------------------------------------------
import os
import sys
import dashloader
import shutil
import config
with open("version.txt") as file:
    D_version=file.read()
if(len(sys.argv)==1 or sys.argv[1]=="version" or sys.argv[1]=="v"):
    print(f"""====== [dashedgeless] ======
[package version]
version: {D_version}
[launcher version]
version: 5.10.1
[command version]
version: 0.0.1
[tools]
7zip 21.07     cscript 5.812
pecmd 201201.88.05.94 X64 Minimum
""")
elif(sys.argv[1]=="help" or sys.argv[1]=="/?" or sys.argv[1]=="-?" or sys.argv[1]=="h" or sys.argv[1]=="-h" or sys.argv[1]=="--help"):
    print(f"""====== [dashedgeless] ======
version: {D_version}

Dashedgeless 命令行工具

Usage:
    dash <command>

Commands:
    cache <插件名称或路径>         缓存一个插件 [包括后缀名]

""")
elif(sys.argv[1]=="cache"):
    if(len(sys.argv)!=3):
        sys.exit(1)
    elif(len(sys.argv[2])>=2 and sys.argv[2][1]==':' and os.path.exists(sys.argv[2])):
        shutil.copyfile(sys.argv[2],config.PLUGIN_PATH+os.path.split(sys.argv[2])[1])
        dashloader.cache_plugin(os.path.split(sys.argv[2])[1])
    elif(os.path.exists(config.PLUGIN_PATH+sys.argv[2])):
        dashloader.cache_plugin(sys.argv[2])
    else:
        print("ERR:文件不存在")
        sys.exit(1)