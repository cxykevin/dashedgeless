import os, random
import config


def find_disk():
    disk_list = "CDEFGHIJKABLMNOPQRSTUVWYZ"
    for i in disk_list:
        this_disk = i + ":"
        if os.path.exists(this_disk + "/Edgeless/version.txt"):
            return this_disk
    raise OSError("Cannot find the Edgeless disk!")


def log(body: str):
    with open(config.LOGS_PATH, "a", encoding="utf-8") as file:
        file.write(body + "\n")


def show_info(body: str):
    rds = str(random.randint(100000, 999999))
    with open(f".tip{rds}.wcs", "w", encoding="gbk") as file:
        file.write(
            f"""TIPS -dummy ?R*-20B*-20
TIPS {config.TITLE},{body},{str(config.INFO_TOUT)},1, 
WAIT {str(config.INFO_TOUT+1000)}
FILE .tip{rds}.wcs
WAIT 1000"""
        )
    os.system(f"start /B {config.PECMD_PATH} .tip{rds}.wcs")
    print("[ info ]" + body)


def show_wrn(body: str):
    rds = str(random.randint(100000, 999999))
    with open(f".tip{rds}.wcs", "w", encoding="gbk") as file:
        file.write(
            f"""TIPS -dummy ?R*-20B*-20
TIPS {config.TITLE},{body},{str(config.INFO_TOUT)},2, 
WAIT {str(config.INFO_TOUT+1000)}
FILE .tip{rds}.wcs
WAIT 1000"""
        )
    os.system(f"start /B {config.PECMD_PATH} .tip{rds}.wcs")
    print("[ wrn  ]" + body)
