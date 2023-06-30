import os
import dashloader
import config


def unpack(zfile, paths):
    dashloader.log("[INFO unpack]" + "unpack [" + zfile + "] => [" + paths + "]")
    rtn = os.system(
        config.SEVENZIP_PATH
        + " x -y -r "
        + '"'
        + zfile
        + '"'
        + " -o"
        + '"'
        + paths
        + '"'
    )
    if rtn != 0:
        dashloader.log("[ERR unpack]" + "7zip error")
