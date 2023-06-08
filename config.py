# coding: utf-8
# get disk
import os,random
def find_disk():
    disk_list="CDEFGHIJKABLMNOPQRSTUVWYZ"
    for i in disk_list:
        this_disk=i+':'
        if(os.path.exists(this_disk+"/Edgeless/version.txt")):
            return this_disk
    raise OSError("Cannot find the Edgeless disk!")
EDGELESS_DISK = find_disk()

# exterior settings
EXT_CONFIG_PATH=f"{EDGELESS_DISK}/Edgeless/dash.py"

# important settings
PLUGIN_PATH=f"{EDGELESS_DISK}/Edgeless/Resource/"
CACHE_PATH=f"{EDGELESS_DISK}/Edgeless/dashedgeless/"
HOOK_PATH=f"{EDGELESS_DISK}/Edgeless/Hooks/onBootFinished/"
VERSION_FILE_PATH="X:/Program Files/Edgeless/dashedgeless/version.txt"
LOADS_PATH="X:/Program Files/Edgeless/"
PROG_PATH="X:/Program Files/"
WHITELIST_PATH="whitelist.txt"
WHITELIST_RPATH="X:/Program Files/Edgeless/dashedgeless/whitelist.txt"
TEMPLATE="template.7z"
TEMPLATE_PATH="X:/Program Files/Edgeless/dashedgeless/template.7z"
HOOK_TEMPLATE="dashedgeless_hook.cmd"
LINK_CMD="mklink"
SEVENZIP_PATH="7z"
WHITELIST_NAME="dash"
PECMD_PATH="pecmd.exe"
DESKTOP_PATH="X:\\Users\\Default\\Desktop\\"
GETLNKINFO_CMD="cscript //NoLogo get_lnkinfo.vbs"
SETLNKINFO_CMD="cscript //NoLogo set_lnkinfo.vbs"
DISABLE_CACHE=False

# info setings
TITLE="[正在加载插件包]"
INFO_TOUT=3000

# log settings
LOGS_PATH="log.log"

# performance settings
THEARD_NUM=16

# UI settings
WIGHT=30


# load ext config file
def log(body:str):
    with open(LOGS_PATH,"a",encoding="utf-8") as file:
        file.write(body+"\n")
def show_err(body:str):
    rds=str(random.randint(100000,999999))
    with open(f".tip{rds}.wcs","w",encoding="gbk") as file:
        file.write(f"""TIPS -dummy ?R*-20B*-20
TIPS {TITLE},{body},{str(INFO_TOUT)},3, 
WAIT {str(INFO_TOUT+1000)}
FILE .tip{rds}.wcs
WAIT 1000""")
    os.system(f"start /B {PECMD_PATH} .tip{rds}.wcs")
    print("[ info ]"+body)
if(not os.path.exists(EXT_CONFIG_PATH)):
    with open(EXT_CONFIG_PATH,"w",encoding="utf-8") as file:
        file.write("""#    Dashedgeless Config File
# the config like this:
#     KEY="value"
# If you want to know more, please use the "dash help config" command
#
# Default settings:
# info setings
  # TITLE="[正在加载插件包]"
  # INFO_TOUT=3000
# log settings
  # LOGS_PATH="log.log"
# performance settings
  # THEARD_NUM=16
# UI settings
  # WIGHT=30
#
print("",end="") # Do not remove this line!



""")

try:
    with open(EXT_CONFIG_PATH,"r",encoding="utf-8") as file:
        strs = file.read()
    exec(strs)
except Exception as r:
    log("[ERR config]Custom error: "+str(r))
    show_err("Load custom config ERROR!\\n  "+str(r).replace(",","，"))

