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
from concurrent.futures import ThreadPoolExecutor

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
        if(os.path.splitext(i)[-1]==".7z" and plugin_size!=template_size and (i not in wlist) and (i[:4]!=config.WHITELIST_NAME)):
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
        if(os.path.splitext(i)[-1]==".7z" and plugin_size==template_size and (i not in wlist) and (i[:3]!=config.WHITELIST_NAME)):
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

def protect_cache(plugin_name:str):
    log("[INFO protect]"+plugin_name)
    def rewrite_cmd(fname):
        log("[INFO rewrite]"+plugin_name+"/"+fname)
        with open(fname,'r') as file:
            flist=file.readlines()
            finally_str="::: [dashedgeless] This .cmd/.bat file was change\n"
            flag=True
            for i in flist:
                left_path=i.upper().replace("\\","/")
                if((config.CACHE_PATH[:-1].upper() in left_path) or (config.LOADS_PATH[:-1].upper() in left_path)):
                    for j in ('REN','DEL','ERASE','RENAME','RMDIR'):
                        if(j+" " in left_path):
                            flag=False
                    if('MOVE' in left_path):
                        i=i.replace("move","copy",1)
                        i=i.replace("Move","Copy",1)
                        i=i.replace("MOVE","COPY",1)
                if(flag):
                    finally_str = finally_str+i+"\n"
        with open(fname,'w') as file:
            file.write(finally_str)
    def rewrite_wcs(fname):
        log("[INFO rewrite]"+plugin_name+"/"+fname)
        try:
            with open(fname,'r') as file:
                flist=file.readlines()
                finally_str="// [dashedgeless] This .wcs file was change\n"
                for i in flist:
                    left_path=i.upper().replace("\\","/")
                    if((config.CACHE_PATH[:-1].upper() in left_path) or (config.LOADS_PATH[:-1].upper() in left_path)):
                        i=i.replace("%ProgramFiles%/Edgeless",config.CACHE_PATH+fname)
                        if('FILE ' in i.upper()):
                            i=i.replace("->","=>",1)
                            if(('=>' not in i) and ('>>' not in i)):
                                continue
                    finally_str = finally_str+i
            with open(fname,'w') as file:
                file.write(finally_str)
        except:
            try:
                with open(fname,'r',encoding="utf=8") as file:
                    flist=file.readlines()
                    finally_str="// [dashedgeless] This .wcs file was change\n"
                    for i in flist:
                        left_path=i.upper().replace("\\","/")
                        if((config.CACHE_PATH[:-1].upper() in left_path) or (config.LOADS_PATH[:-1].upper() in left_path)):
                            i=i.replace("%ProgramFiles%/Edgeless",config.CACHE_PATH+fname)
                            if('FILE ' in i.upper()):
                                i=i.replace("->","=>",1)
                                if(('=>' not in i) and ('>>' not in i)):
                                    continue
                        finally_str = finally_str+i
                with open(fname,'w',encoding="utf=8") as file:
                    file.write(finally_str)
            except:
                log("[ERR rewrite]"+plugin_name+"/"+fname)
    unpack=os.listdir(config.CACHE_PATH+plugin_name)
    for i in unpack:
        if(os.path.isfile(config.CACHE_PATH+plugin_name+"/"+i)):
            fname=config.CACHE_PATH+plugin_name+"/"+i
            if(os.path.splitext(i)[-1]==".cmd"):
                rewrite_cmd(fname)
            if(os.path.splitext(i)[-1]==".bat"):
                rewrite_cmd(fname)
            if(os.path.splitext(i)[-1]==".wcs"):
                rewrite_wcs(fname)

def load_plugin(plugin_name:str):
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
                returned = os.system(config.LINK_CMD+" "+'"'+(config.LOADS_PATH+i)+'"'+" "+'"'+(config.CACHE_PATH+plugin_name+"/"+i)+'"')
                if(returned != 0):
                    log("[WRN link]"+"link error["+config.LINK_CMD+" "+'"'+(config.LOADS_PATH+i)+'"'+" "+'"'+(config.CACHE_PATH+plugin_name+"/"+i)+'"'+"]")
        for i in cmdlist:
            returnd = os.system('"'+i+'"')
            log("[INFO run]"+plugin_name+"/"+i+" [returned "+str(returnd)+"]")
        for i in wcslist:
            returnd = os.system(f"start /B {config.PECMD_PATH}"+' "'+i+'"')
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

def loads():
    sethook()
    log("[INFO start]"+"start load")
    pluglist = get_cache_list()
    if(config.THEARD_NUM==0):
        for i in pluglist:
            load_plugin(i)
        log("[INFO end]"+"(single threaded) plugins loaded")
    else:
        def load_plugin_theard(page):
            while(len(pluglist)!=0):
                this_theard=pluglist.pop()
                load_plugin(this_theard)
                log("[INFO theard]"+"theard["+str(i)+"] load plugin["+this_theard+"]")
            log("[INFO theard]"+"theard["+str(i)+"] exit")
        with ThreadPoolExecutor(max_workers=config.THEARD_NUM) as t:
            for i in range(config.THEARD_NUM):
                log("[INFO theard]"+"start theard "+str(i))
                t.submit(load_plugin_theard,i)

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
    log("[INFO cache]"+"protect plugin["+name+"]")
    protect_cache(name)

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
    print("you can import in Python and call it")
    print("-------------------------------------------")
