import numpy as np
import pandas as pd


def temperature(actual_date,
                daily_amplitude = 3,
                seasonal_amplitude = 10,
                annual_mean = 9.5,
                mu = 0,
                sd = 3):

    actual_date = pd.to_datetime(actual_date)

    # proportion of hours of a day
    hour = np.array(actual_date.hour + actual_date.minute/60)

    # proportion of
    month = np.array(actual_date.month + actual_date.day/30 + actual_date.hour/24)

    # normal distributed measurement error
    measurement_error = np.random.normal(mu, sd, size = len(actual_date))

    # daily pattern, depending on the portion of hours of a day
    daily_effect = daily_amplitude * np.sin(2*np.pi * hour / 24)

    # seasonal pattern over the year
    seasonal_effect = seasonal_amplitude * np.sin(2* np.pi* (month-4.5)/ 12 )

    # additive composition of the actual soil moisture
    actual_temperature = annual_mean + daily_effect + seasonal_effect + measurement_error

    return actual_temperature


def moisture(actual_date,
             annual_mean=27,
             daily_amplitude=2,
             seasonal_amplitude=5,
             mu=0,
             sd=2):
    actual_date = pd.to_datetime(actual_date)

    # proportion of hours of a day
    hour = np.array(actual_date.hour + actual_date.minute / 60)

    # proportion
    month = np.array(actual_date.month + actual_date.day / 30 + actual_date.hour / 24)

    # normal distributed measurement error
    measurement_error = np.random.normal(mu, sd, size=len(actual_date))

    # daily pattern, depending on the portion of hours of a day
    daily_effect = daily_amplitude * np.sin(2 * np.pi * hour / 24)

    # seasonal pattern over the year
    seasonal_effect = seasonal_amplitude * np.sin(2 * np.pi * month / 12)

    # additive composition of the actual soil moisture
    actual_moisture = annual_mean + daily_effect + seasonal_effect + measurement_error
    # cut-off, moisture can not be negative
    np.place(actual_moisture, actual_moisture < 0, 0)

    return actual_moisture


def battery(time, average_LT = 30):
    time = pd.to_datetime(time)
    # timedifference in days
    timediff = (time-time.min()).astype(int)/((10**9)*60*60*24)
    # time difference modulo the average_LT
    timediff = timediff % average_LT
    percentage = 100 - (100/average_LT) * timediff
    return percentage
