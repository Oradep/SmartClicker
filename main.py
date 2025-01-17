import keyboard
import mouse
import time
import random
import threading

isClicking = False

ClickCooldown = 0.3
onColdown = False
double = True

clicksX = []
clicksY = []
LastClick = time.time()
ProfilingStartTime = time.time()


config = { 
    'double_click': 11,
    'single_click': 5,
    'double_time_min': 10,
    'double_time_max': 40,
    'single_time_min': 5,
    'single_time_max': 20,
    'range': 3, #какой частью от значения будет разброс

    'key': 'F6'
}




def clicker():
    global isClicking
    global onColdown
    while True:
        if isClicking and not onColdown:
            mouse.click(button = 'left')
            Cooldown()

def clicker_mode():
    global double
    while True:
        if double:
            time.sleep(random.uniform(config['double_time_min'], config['double_time_max']))
        else:
            time.sleep(random.uniform(config['single_time_min'], config['single_time_max']))
            double = True



def Cooldown():
    global config
    global ClickCooldown
    global double
    if double:
        ClickCooldown = 1 / (config['double_click'] + random.uniform(config['double_click']/config['range'],-(config['double_click']/config['range'])))
    else:
        ClickCooldown = 1 / (config['single_click'] + random.uniform(config['single_click']/config['range'],-(config['single_click']/config['range'])))
    time.sleep(ClickCooldown)



def set_clicker():
    global isClicking
    if isClicking:
        isClicking = False
        print('Off')
    else:
        isClicking = True
        print('On')



keyboard.add_hotkey(config['key'], set_clicker)

thread1 = threading.Thread(target=clicker, name="Кликер")
thread2 = threading.Thread(target=clicker_mode, name="Смена режима кликера")

thread1.start()
thread2.start()