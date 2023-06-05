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
if(os.path.exists(config.VERSION_FILE_PATH)):
    with open(config.VERSION_FILE_PATH) as file:
        D_version=file.read()
else:
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
本工具为对ept功能的封装，加入了 dashedgeless 的功能
若命令不存在，将自动转交至 ept
您可以使用 dash 命令替换 ept 命令（部分命令语法可能改变）
以下标有 “[ ]” 的功能即为 ept 原有功能 

Usage:
    dash <command>

Commands:
    install <插件名称或路径>        安装插件  当输入无效时会将输入内容作为关键词提交给 ept search
    autoclean                       清理插件缓存  删除已更新/已删除的插件的缓存（不会处理白名单插件）
    upgrade                         查找插件的可用更新，对名称不规范的插件包进行提示，并清理缓存
    remove <插件名称>               永久移除指定的插件（重启生效）
    update                          [更新插件索引]  更新本地的插件索引文件
    search <插件名>                 [搜索插件]  使用关键词查找指定插件的序号
    getver <插件名>                 [获取插件版本]

""")
elif(sys.argv[1]=="install"):
    if(len(sys.argv)!=3):
        sys.exit(1)
    pname=sys.argv[2]
    if(pname[0]=='"'):
        pname=pname[1:-1]
    elif((len(pname)>=1 and pname[0]=='.') or (len(pname)>=2 and pname[1]==':' and os.path.exists(pname))):
        print("INFO:安装一个本地文件")
        shutil.copyfile(pname,config.PLUGIN_PATH+os.path.split(pname)[1])
        dashloader.cache_plugin(os.path.split(pname)[1])
        dashloader.set_icon()
    elif(os.path.exists(config.PLUGIN_PATH+pname)):
        print("INFO:安装一个已有插件包")
        dashloader.cache_plugin(pname)
        dashloader.set_icon()
    else:
        print("WRN:找不到本地文件")
        print("INFO:尝试运行ept")
        returns=os.system("ept-install "+'"'+pname+'"'+" -a")
        if(returns!=0):
            print("ERR:文件/插件不存在")
            sys.exit(1)
        else:
            print("INFO:开始缓存插件")
            dashloader.caches()
            dashloader.set_icon()
elif(sys.argv[1]=="autoclean"):
    print("INFO:开始清理")
    c_list=dashloader.get_cache_list()
    f_list=os.listdir(config.CACHE_PATH)
    for i in f_list:
        if(i not in c_list):
            paths=config.CACHE_PATH+i
            print("INFO:清理缓存 ["+paths+"]")
            shutil.rmtree(paths)
    print("INFO:开始清理失效插件")
    for i in c_list:
        if(i not in f_list and (i+'f') not in f_list):
            paths=config.PLUGIN_PATH+i
            print("INFO:清理插件 ["+paths+"]")
            os.remove(paths)
    print("INFO:清理完成")
elif(sys.argv[1]=="upgrade"):
    print("INFO:运行 ept")
    returns=os.system("ept upgrage")
    print("INFO:开始缓存插件")
    c_list=dashloader.caches()
    print("INFO:开始清理")
    c_list=dashloader.get_cache_list()
    f_list=os.listdir(config.CACHE_PATH)
    for i in f_list:
        if(i not in c_list):
            paths=config.CACHE_PATH+i
            print("INFO:清理缓存 ["+paths+"]")
            shutil.rmtree(paths)
    print("INFO:开始清理失效插件")
    for i in c_list:
        if(i not in f_list and (i+'f') not in f_list):
            paths=config.PLUGIN_PATH+i
            print("INFO:清理插件 ["+paths+"]")
            os.remove(paths)
    print("INFO:清理完成")
    print("INFO:更新完成")
elif(sys.argv[1]=="remove"):
    if(len(sys.argv)!=3):
        sys.exit(1)
    pname=sys.argv[2]
    if(pname[0]=='"'):
        pname=pname[1:-1]
    if(not os.path.exists(config.PLUGIN_PATH+pname)):
        print("ERR:找不到文件")
        sys.exit(1)
    print("INFO:运行 ept")
    returns=os.system("ept remove "+'"'+pname.split("_")[0]+'"'+" -a")
    print("INFO:清理插件源文件")
    os.remove(config.PLUGIN_PATH+pname)
    if(os.path.exists(config.CACHE_PATH+pname)):
        print("INFO:清理插件缓存")
        shutil.rmtree(config.CACHE_PATH+pname)
elif(sys.argv[1]=="list"):
    def get_whitelist():
        with open(config.WHITELIST_PATH,encoding="utf-8") as file:
            wlist = file.readlines()
        return wlist
    print(" Plugin                                            |  Status")
    print("-------------------------------------------------------------")
    plist = os.listdir(config.PLUGIN_PATH)
    template_size=os.path.getsize(config.TEMPLATE)
    wlist=get_whitelist()
    outlist=[]
    for i in plist:
        plugin_size=os.path.getsize(config.PLUGIN_PATH+i)
        if(os.path.splitext(i)[-1]==".7z"):
            if(i[:4]==config.WHITELIST_NAME):
                status = "   Dashedgeless"
            elif((i+"n") in wlist):
                status = "[*]Whitelist"
            elif(plugin_size==template_size):
                status = "[+]Cached"
            else:
                status = "[-]Default"
            print("{:50}{:20}".format(i,status))
        if(os.path.splitext(i)[-1]==".7zf"):
            if(plugin_size==template_size):
                status = "[*]Disable(Cached)"
            else:
                status = "[*]Disable(Default)"
            print("{:50}{:20}".format(i,status))
elif(sys.argv[1]=="search"):
    if(len(sys.argv)!=3):
        sys.exit(1)
    pname=sys.argv[2]
    if(pname[0]=='"'):
        pname=pname[1:-1]
    print("INFO:运行 ept")
    returns=os.system("ept search "+'"'+pname+'"')
    sys.exit(returns)
elif(sys.argv[1]=="upload"):
    print("INFO:运行 ept")
    returns=os.system("ept upload")
    sys.exit(returns)
elif(sys.argv[1]=="getver"):
    if(len(sys.argv)!=3):
        sys.exit(1)
    pname=sys.argv[2]
    if(pname[0]=='"'):
        pname=pname[1:-1]
    print("INFO:运行 ept")
    returns=os.system("ept getver "+'"'+pname+'"')
    sys.exit(returns)
elif(sys.argv[1]=="dev"):
    print("WRN:本功能为开发者使用，普通用户请勿使用")
    if(len(sys.argv)!=3):
        sys.exit(1)
    if(sys.argv[2]=="install"):
        print("INFO:安装/更新程序到启动盘")
        E_disk=dashloader.find_disk()
        print("INFO:当前启动盘 ["+E_disk+"]")
        shutil.copyfile(f"dist/dashedgeless_{D_version}_dashedgeless (bot).7z",config.PLUGIN_PATH+f"dashedgeless_{D_version}_dashedgeless (bot).7z")
        print("INFO:安装完成")
    if(sys.argv[2]=="build"):
        print("INFO:编译程序")
        sys.exit(os.system("cmd /C build"))
    if(sys.argv[2]=="onload"):
        print("INFO:onload模式启动")
        dashloader.caches()