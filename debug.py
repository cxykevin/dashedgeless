import ui
import time

ui.sets(0, 20)
for i in range(0, 20):
    time.sleep(1)
    ui.sets(i, 20)
