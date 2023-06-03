# coding: utf-8
import config
import os
import random

def show_info(body:str):
    rds=str(random.randint(100000,999999))
    with open(f".tip{rds}.wcs","w",encoding="gbk") as file:
        file.write(f"""TIPS -dummy ?R*-20B*-20
TIPS {config.TITLE},{body},{str(config.INFO_TOUT)},1, 
WAIT {str(config.INFO_TOUT+1000)}
FILE .tip{rds}.wcs
WAIT 1000""")
    os.system(f"start /B {config.PECMD_PATH} .tip{rds}.wcs")
    print("[ info ]"+body)
def log(body:str):
    with open(config.LOGS_PATH,"a",encoding="utf-8") as file:
        file.write(body+"\n")

log("[INFO ui]"+"ui load")

def sets(a:int,b:int):
    if(b==0):
        k=0
    else:
        k=a/b
    wights=int(config.WIGHT-config.WIGHT*k)
    show_info("[dash] "+str(a)+"/"+str(b)+" ["+('>'*(config.WIGHT-wights))+('='*wights)+"]")

def finish():
    show_info("[dash] 加载完成！")