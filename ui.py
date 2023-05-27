# coding: utf-8
import tkinter
import config
from threading import Thread

def log(body:str):
    with open(config.LOGS_PATH,"a",encoding="utf-8") as file:
        file.write(body+"\n")
window=tkinter.Tk()
window.title(config.TITLE)
window.geometry(f"{config.WIGHT}x{config.HEIGHT}+{window.winfo_screenwidth()-config.WIGHT-config.RIGHT}+{config.TOP}")
window.overrideredirect(True)
window.configure(bg='#FFFFFF')
canvas = tkinter.Canvas(window, bg="#FFFFFF", borderwidth=0, relief="flat")
canvas.place(x=0,y=0,width=config.WIGHT,height=config.HEIGHT)
rect = canvas.create_rectangle(config.WIGHT,0,config.WIGHT,config.HEIGHT,fill="#9DE0FF",outline='#9DE0FF')
rect2 = canvas.create_rectangle(config.WIGHT,0,4,config.HEIGHT,fill="#32D3FF",outline='#32D3FF')
text = canvas.create_text(config.WIGHT/2,config.HEIGHT/2,text="No Data",fill="#20B0D0")
def on_run(*args,**kwargs):
    log("[INFO ui]"+"ui theard start")
    while 1:
        try:
            window.update()
        except:
            break
log("[INFO ui]"+"ui theard load")
def load_window():
    global t1
    t1=Thread(target=on_run, args=('dashedgeless_cache_window', 1))
    t1.start()
def change(x:int):
    canvas.coords(rect,x,0,config.WIGHT,config.HEIGHT)
    canvas.coords(rect2,x,0,x+2,config.HEIGHT)
def sets(a:int,b:int):
    if(b==0):
        k=0
    else:
        k=a/b
    change(int(config.WIGHT-config.WIGHT*k))
    canvas.itemconfigure(text, text=str(a)+" / "+str(b))
    window.update()
def del_window():
    log("[INFO ui]"+"ui theard stop")
    window.destroy()
    t1.join()

