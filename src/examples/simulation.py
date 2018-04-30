#!/usr/bin/env python3.6

import numpy as np
np.set_printoptions(threshold=np.inf)
import pandas as pd
from time import sleep
import json
from utils import moisture, temperature, battery


time = np.array(pd.date_range('20170101', periods=15000, freq='0.5H'))

moisture_sensor = moisture(time)
temp_sensor = temperature(time)
battery_sensor = battery(time)

data = {'moisture': moisture_sensor, 'temp': temp_sensor, 'battery': battery_sensor}

sensor_data = pd.DataFrame(data, index=time)
rows = moisture_sensor.shape

# Support of json events or individual rows
for i in range(rows[0]):
    event = {'time': i%5,
             'moisture': sensor_data.moisture[i],
             'temp': sensor_data.temp[i],
             'battery': sensor_data.battery[i]}
    #print(event)
    print('{} {} {} {}'.format(i%5, sensor_data.moisture[i], sensor_data.temp[i], sensor_data.battery[i]))
    sleep(1)

# pipe this script
# ./03_simulation.py |  nc -lk 9999
