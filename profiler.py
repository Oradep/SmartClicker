import keyboard
import mouse
import time
import matplotlib.pyplot as plt
import numpy as np
from scipy import interpolate
from scipy.interpolate import interp1d
import json


isProfiling = False
clicksX = []
clicksY = []
LastClick = time.time()
ProfilingStartTime = time.time()


def set_profiler():
	global isProfiling
	global ProfilingStartTime
	if isProfiling:
		isProfiling = False
		print('Profiler off')
		savelog(clicksX, clicksY)
		mouse.unhook_all()
	else:
		isProfiling = True
		ProfilingStartTime = time.time()
		print('Profiler on (F7 to stop)')
		mouse.on_click(DetectClick, args=())




def DetectClick():
	global isProfiling
	if isProfiling:
		global ProfilingStartTime
		global LastClick
		TimeFromStart = round((time.time() - ProfilingStartTime), 5)
		x = TimeFromStart
		y = round(1/(time.time() - LastClick), 5)
		if len(clicksX) < 2:
			clicksX.append(x)
			clicksY.append(5)	
		elif y > 5 and y<20:
			clicksX.append(x)
			clicksY.append(y)	
		LastClick = time.time()


def createplot():
	x, y = readlog()
	interp = interpolate.interp1d(x, y, kind='linear')
	X_ = list(np.linspace(min(x), max(x), len(x)*10))
	Y_ = list(interp(X_))
	plt.plot(X_, Y_)
	plt.xlabel('Время') #Подпись для оси х
	plt.ylabel('КПС')
	plt.show()


def readlog():
	fx = open('logX.txt')
	fy = open('logY.txt')
	x = fx.readlines()
	y = fy.readlines()
	fx.close()
	fy.close()
	for i in x:
		x[x.index(i)] = float(x[x.index(i)])
	for i in y:
		y[y.index(i)] = float(y[y.index(i)])
	return x, y


def savelog(x, y):
	f = open('logX.txt', 'w')
	f.writelines("%s\n" % i for i in x)
	f.close()

	f = open('logY.txt', 'w')
	f.writelines("%s\n" % i for i in y)
	f.close()

	print('Сохранить как новый конфиг для кликера? y/n')
	input('')
	print(pickle.dumps(interp, f))
	if input == 'y':
		interp = interpolate.interp1d(x, y, kind='linear')
		print(json.dumps(interp))



print('Нажмите F7 чтобы запустить новый профайлер')
print('Нажмите F8, чтобы отобразить данные последнего профилирования')
keyboard.add_hotkey('F7', set_profiler)
keyboard.add_hotkey('F8', createplot)


input()