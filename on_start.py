# coding: utf-8
import dashloader
import config
import os, sys
import time
from concurrent.futures import ProcessPoolExecutor, wait, ALL_COMPLETED
from multiprocessing import freeze_support

pluglist = dashloader.get_cache_list()

if __name__ == "__main__":
    freeze_support()
    dashloader.log("[INFO path]" + "set dash path")
    os.system("pecmd setpath.wcs")
    time.sleep(1)
    if dashloader.config.THEARD_NUM == 0:
        dashloader.log("[INFO start]" + "(single thread) start load")
        for i in pluglist:
            dashloader.load_plugin(i)
    else:
        plist = dashloader.get_cache_list()
        dashloader.log("[INFO start]" + "start load")
        with ProcessPoolExecutor(max_workers=config.THEARD_NUM) as t:
            for i in range(config.THEARD_NUM):
                dashloader.log("[INFO theard]" + "start theard " + str(i))
                t.submit(
                    dashloader.load_plugin_theard,
                    i,
                    [plist[j] for j in range(i, len(plist), config.THEARD_NUM)],
                )
            t.shutdown()
    if config.DISABLE_CACHE:
        sys.exit(0)
    time.sleep(3)
    dashloader.log("[INFO start]" + "load plugin finished")
    dashloader.set_icon()
    dashloader.log("[INFO start]" + "fix icon finished")
    time.sleep(6)
    dashloader.caches()
