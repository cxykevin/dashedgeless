# coding: utf-8
#          [dashedgeless] main file
# ------  Welcome to [dashedgeless]!  -------
# this program cannot run only, please use the
# 'dash' command or install this plugin
# you can import in Python and call it
# -------------------------------------------
import os
import random
import shutil
from concurrent.futures import ThreadPoolExecutor,wait,ALL_COMPLETED

import config # load config
import ui # load GUI
import unpack # load unpack 7z tools

def find_disk():
    disk_list="CDEFGHIJKABLMNOPQRSTUVWYZ"
    for i in disk_list:
        this_disk=i+':'
        if(os.path.exists(this_disk+"/Edgeless/version.txt")):
            return this_disk
    raise OSError("Cannot find the Edgeless disk!")


def log(body:str):
    with open(config.LOGS_PATH,"a",encoding="utf-8") as file:
        file.write(body+"\n")

def get_whitelist():
    with open(config.WHITELIST_PATH,encoding="utf-8") as file:
        wlist = file.readlines()
    return wlist

def get_plugin_list():
    log("[INFO plugin]")
    plist = os.listdir(config.PLUGIN_PATH)
    template_size=os.path.getsize(config.TEMPLATE)
    wlist=get_whitelist()
    outlist=[]
    for i in plist:
        plugin_size=os.path.getsize(config.PLUGIN_PATH+i)
        if(os.path.splitext(i)[-1]==".7z" and plugin_size!=template_size and ((i+"\n") not in wlist) and (i[:4]!=config.WHITELIST_NAME)):
            outlist.append(i)
    return outlist

def get_cache_list():
    log("[INFO cache]")
    plist = os.listdir(config.PLUGIN_PATH)
    template_size=os.path.getsize(config.TEMPLATE)
    wlist=get_whitelist()
    outlist=[]
    for i in plist:
        plugin_size=os.path.getsize(config.PLUGIN_PATH+i)
        if(os.path.splitext(i)[-1]==".7z" and plugin_size==template_size and ((i+"\n") not in wlist) and (i[:3]!=config.WHITELIST_NAME)):
            outlist.append(i)
    return outlist

def show_info(body:str):
    rds=str(random.randint(100000,999999))
    with open(f".tip{rds}.wcs","w",encoding="gbk") as file:
        file.write(f"""TIPS -dummy ?R*-20B*-20
TIPS {config.TITLE},{body},{str(config.INFO_TOUT)},1, 
WAIT {str(config.INFO_TOUT+1000)}
FILE .tip{rds}.wcs""")
    os.system(f"start /B {config.PECMD_PATH} .tip{rds}.wcs")
    print("[ info ]"+body)

def show_wrn(body:str):
    rds=str(random.randint(100000,999999))
    with open(f".tip{rds}.wcs","w",encoding="gbk") as file:
        file.write(f"""TIPS -dummy ?R*-20B*-20
TIPS {config.TITLE},{body},{str(config.INFO_TOUT)},2, 
WAIT {str(config.INFO_TOUT+1000)}
FILE .tip{rds}.wcs""")
    os.system(f"start /B {config.PECMD_PATH} .tip{rds}.wcs")
    print("[ wrn  ]"+body)

def load_plugin(plugin_name:str):
    def d_link(p_name:str,dir_name:str):
        def dfs(paths:tuple,p_name:str):
            path_str='/'.join(paths)
            os.mkdir(config.LOADS_PATH+path_str)
            for i in os.listdir(config.CACHE_PATH+p_name+"/"+path_str):
                if(os.path.isfile(config.CACHE_PATH+p_name+"/"+path_str+"/"+i)):
                    os.system(config.LINK_CMD+" "+'"'+(config.LOADS_PATH+path_str+"/"+i)+'"'+" "+'"'+(config.CACHE_PATH+plugin_name+"/"+path_str+"/"+i)+'"'+" >nul")
                else:
                    dfs(paths+(i,),p_name)
        dfs((dir_name,),p_name)
    if(os.path.exists(config.CACHE_PATH+plugin_name)):
        log("[INFO load]"+config.PLUGIN_PATH+plugin_name)
        show_info(plugin_name)
        unpack=os.listdir(config.CACHE_PATH+plugin_name)
        cmdlist=[]
        wcslist=[]
        for i in unpack:
            if(os.path.isfile(config.CACHE_PATH+plugin_name+"/"+i)):
                if(os.path.splitext(i)[-1]==".cmd"):
                    cmdlist.append(config.CACHE_PATH+plugin_name+"/"+i)
                if(os.path.splitext(i)[-1]==".bat"):
                    cmdlist.append(config.CACHE_PATH+plugin_name+"/"+i)
                if(os.path.splitext(i)[-1]==".wcs"):
                    wcslist.append(config.CACHE_PATH+plugin_name+"/"+i)
            else:
                d_link(plugin_name,i)
        for i in cmdlist:
            returnd = os.system('"'+i+'"')
            log("[INFO run]"+plugin_name+"/"+i+" [returned "+str(returnd)+"]")
        for i in wcslist:
            returnd = os.system(f"{config.PECMD_PATH}"+' "'+i+'"')
            log("[INFO run]"+plugin_name+"/"+i+" [returned "+str(returnd)+"]")
    else:
        show_wrn("!"+plugin_name)
        log("[WRN load]"+"!"+plugin_name)

def sethook():
    if(not os.path.exists(config.HOOK_PATH)):
        os.mkdir(config.HOOK_PATH)
    if(not os.path.exists(config.HOOK_PATH+config.HOOK_TEMPLATE)):
        log("[INFO hook]"+"set hook")
        shutil.copyfile(config.HOOK_TEMPLATE, config.HOOK_PATH+config.HOOK_TEMPLATE)

def set_icon():
    for i in os.listdir(config.DESKTOP_PATH):
        if(os.path.splitext(i)[1].upper()==".LNK"):
            with os.popen(config.GETLNKINFO_CMD+" "+'"'+config.DESKTOP_PATH+'"'+" "+'"'+i+'"') as pops:
                this_info_list=pops.readlines()
            info_list=this_info_list[0][:-1]
            if(os.path.islink(info_list)):
                icon_s=os.readlink(info_list)[4:]
                log("[INFO fixicon]"+"fix icon["+i+"] => ["+icon_s+"]")
                os.system(config.SETLNKINFO_CMD+" "+'"'+config.DESKTOP_PATH+'"'+" "+'"'+i+'"'+" "+'"'+icon_s+'"')

def loads():
    sethook()
    pluglist = get_cache_list()
    if(config.THEARD_NUM==0):
        log("[INFO start]"+"(single thread) start load")
        for i in pluglist:
            load_plugin(i)
    else:
        log("[INFO start]"+"start load")
        def load_plugin_theard(page):
            while(len(pluglist)!=0):
                this_theard=pluglist.pop()
                log("[INFO theard]"+"theard["+str(i)+"] load plugin["+this_theard+"]")
                load_plugin(this_theard)
            log("[INFO theard]"+"theard["+str(i)+"] exit")
        tasklist=[]
        with ThreadPoolExecutor(max_workers=config.THEARD_NUM) as t:
            for i in range(config.THEARD_NUM):
                log("[INFO theard]"+"start theard "+str(i))
                tasklist.append(t.submit(load_plugin_theard,i))
        wait(tasklist, return_when=ALL_COMPLETED)
    log("[INFO start]"+"load plugin finished")
    set_icon()
    log("[INFO start]"+"fix icon finished")

def cache_plugin(name):
    log("[INFO cache]"+"cache plugin["+name+"]")
    if(os.path.exists(config.CACHE_PATH+name)):
        log("[INFO cache]"+"remove old plugin["+name+"]")
        shutil.rmtree(config.CACHE_PATH+name)
    os.mkdir(config.CACHE_PATH+name)
    unpack.unpack(config.PLUGIN_PATH+name,config.CACHE_PATH+name)
    os.remove(config.PLUGIN_PATH+name)
    log("[INFO cache]"+"copy plugin template["+config.PLUGIN_PATH+name+"]")
    shutil.copyfile(config.TEMPLATE,config.PLUGIN_PATH+name)

def caches():
    log("[INFO cache]"+"start cache")
    plist = get_plugin_list()
    ui.load_window()
    ui.sets(0,len(plist))
    j=0
    for i in plist:
        cache_plugin(i)
        j+=1
        ui.sets(j,len(plist))
    

if __name__=="__main__":
    print("------  Welcome to [dashedgeless]!  -------")
    print("this program cannot run only, please use the 'dash' command or install this plugin")
    print("you can import it in Python and call it")
    print("-------------------------------------------")
