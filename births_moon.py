#make plots for births over dates
import openpyxl, os, datetime
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from fullmoon import NextFullMoon
from fullmoon import IsFullMoon

from scipy.signal import savgol_filter

"""
create debug environment
"""
import logging
logging.basicConfig(level=logging.DEBUG, format=' %(asctime)s - %(levelname)s- %(message)s')
logging.disable(logging.CRITICAL)

# file including all daily births
file = 'births.xlsx'

data = pd.ExcelFile(file)
df = data.parse('TF_BIRTHS')

ps = openpyxl.load_workbook('births.xlsx')
sheet = ps['TF_BIRTHS']


# make empty vectors of births
a = range(1992,2020,4)

for i in range(1992,2020):
    if i in a:
        logging.debug('Initiate vectors of births, dates and moons for year (%s)' %(i))
        globals()["births_" + str(i)] = [0]*366
        globals()["dates_" + str(i)] = [0]*366
        globals()["moons_" + str(i)] = [0]*40
    else:
        globals()["births_" + str(i)] = [0]*365
        globals()["dates_" + str(i)] = [0]*365
        globals()["moons_" + str(i)] = [0]*40

j = 0
k = 0

for i in range(1,sheet.max_row):
    j += 1
    globals()["births_" + str(1992 + k)][j-1] = sheet['B' + str(i+1)].value
    if 1992+k in a:
        if (j % 366) == 0:
                k += 1
                j = 0
    else:
        if (j%365)== 0:
                k += 1
                j = 0


#date1 = '2019-01-01'
#date2 = '2019-12-31'

# find the fullmoons
n = NextFullMoon()
n_moon = n.set_origin_date_string('1992-01-01').next_full_moon().date()   #next moon

for i in range(1992,2020):
    j = 0
    k = 0
    date1 =  str(i)+"-01-01"
    date2 =  str(i)+"-12-31"

    start = datetime.datetime.strptime(date1, '%Y-%m-%d')
    end = datetime.datetime.strptime(date2, '%Y-%m-%d')
    step = datetime.timedelta(days=1)
    while start <= end:
            globals()["dates_"+str(i)][j] = start.date()
            if start.date() == n_moon:
                logging.critical('full moon date (%s)' %(n_moon))
                globals()["moons_"+str(i)][k] = n_moon
                n_moon +=step
                n_moon = n.set_origin_date_string(str(n_moon)).next_full_moon().date()
                k +=1
            start += step
            j += 1
    globals()["moons_"+str(i)] = np.trim_zeros(globals()["moons_"+str(i)])



for i in range(1992,1999):
     plt.figure(i-1993)
     plt.plot(globals()["dates_"+str(i)], globals()["births_"+str(i)])
       #plt.plot([globals()["moons_"+str(i)][0],globals()["births_"+str(i)][0]], [100,400])
     for j in range(0,len(globals()["moons_"+str(i)])):
         plt.axvline(x = globals()["moons_"+str(i)][j], color = 'r', linewidth=.7 )

plt.show()

"""
for i in range(1994,1995):
       plt.plot(globals()["dates_"+str(i)], globals()["births_"+str(i)])
       #plt.plot([globals()["moons_"+str(i)][0],globals()["births_"+str(i)][0]], [100,400])
       for j in range(0,len(globals()["moons_"+str(i)])-1):
           plt.axvline(x = globals()["moons_"+str(i)][j], color = 'r', linewidth=.7 )

plt.show()
"""

