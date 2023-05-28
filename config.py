# coding: utf-8
# get disk
import os
def find_disk():
    disk_list="CDEFGHIJKABLMNOPQRSTUVWYZ"
    for i in disk_list:
        this_disk=i+':'
        if(os.path.exists(this_disk+"/Edgeless/version.txt")):
            return this_disk
    raise OSError("Cannot find the Edgeless disk!")
EDGELESS_DISK = find_disk()

# important settings
PLUGIN_PATH=f"{EDGELESS_DISK}/Edgeless/Resource/"
CACHE_PATH=f"{EDGELESS_DISK}/Edgeless/dashedgeless/"
HOOK_PATH=f"{EDGELESS_DISK}/Edgeless/Hooks/onBootFinished/"
LOADS_PATH="X:/Program Files/Edgeless/"
PROG_PATH="X:/Program Files/"
WHITELIST_PATH="whitelist.txt"
TEMPLATE="template.7z"
HOOK_TEMPLATE="dashedgeless_hook.cmd"
LINK_CMD="mklink"
SEVENZIP_PATH="7z"
WHITELIST_NAME="dash"
PECMD_PATH="pecmd.exe"
DESKTOP_PATH="X:\\Users\\Default\\Desktop\\"
GETLNKINFO_CMD="cscript //NoLogo get_lnkinfo.vbs"
SETLNKINFO_CMD="cscript //NoLogo set_lnkinfo.vbs"

# info setings
TITLE="[正在加载插件包]"
INFO_TOUT=3000

# log settings
LOGS_PATH="log.log"

# performance settings
THEARD_NUM=0

# GUI settings
WIGHT=100
HEIGHT=40
RIGHT=40
TOP=40
