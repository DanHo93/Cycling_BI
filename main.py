
from fitparse import FitFile
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import glob
import numpy
import numpy as np
from sklearn.linear_model import LinearRegression


mypath = ""
directory = mypath + "/*.fit"

#Funktionen
def importFiles(searchName):
    allFiles = (glob.glob(searchName))
    return allFiles

def getFitData(allFiles):
    df = []
    for i in allFiles:
        fitfile = FitFile(i)

        while True:
            try:
                fitfile.messages
                break
            except KeyError:
                continue
        workout = []
        for record in fitfile.get_messages('record'):
            r = {}
            for record_data in record:
                r[record_data.name] = record_data.value
            workout.append(r)
        df.append(pd.DataFrame(workout))
    return df

def printOverview():
    descData = []
    print("Datensätze: ",len(dfs))
    for i in dfs:
        print(i.head())

    count = 0
    for i in dfs:
        #print("Datensatz Nr.: ", count + 1)
        descData.append(i[['timestamp', 'power', 'heart_rate', 'cadence']].describe())
        #print(descData[count])
        count = count + 1
    return descData

def heartRate(df):
    fig, ax = plt.subplots()
    df[['heart_rate']].plot(ax=ax)
    #ax.legend()
    ax.set_axisbelow(True)
    ax.minorticks_on()
    #ax.grid(which='major', linestyle='-', linewidth='0.5', color='red')
    #ax.grid(which='minor', linestyle=':', linewidth='0.5', color='black')
    plt.show()

def meanCalcHeartRate(df):
    return df["heart_rate"].mean()


def meanCalcCadence(df):
    return df["cadence"].mean()

def meanCalcPower(df):
    return df["power"].mean()

def plotPower(df):
    ax = df['power'].plot()
    ticklabels = df.index.strftime('%Y-%m-%d')
    ax.xaxis.set_major_formatter(ticker.FixedFormatter(ticklabels))
    ax.yaxis.set_major_formatter(ticker.FormatStrFormatter('%.2f'))
    plt.show()

def formRelevantDataFrame(df):
    df = pd.DataFrame(data = df)
    df = df.drop(['battery_soc', 'left_pedal_smoothness', 'left_torque_effectiveness', 'temperature'], axis= 1)
    df['timestamp'] = pd.to_datetime(df['timestamp'], format="%d.%m.%Y %H:%M:%S.%f")
    df.set_index('timestamp', inplace=True)
    return df


def addHeartrateToDataframe(dfs):
    meanHeartRateOfWorkouts = []
    for i in dfs:
        meanHeartRateOfWorkouts.append(meanCalcHeartRate(i))
    print(meanHeartRateOfWorkouts)
    workoutsDf.insert(column = "HeartRate", value = meanHeartRateOfWorkouts, loc = 1)
    return workoutsDf

def addCadenceToDataframe(dfs):
    meanCadenceOfWorkouts = []
    for i in dfs:
        meanCadenceOfWorkouts.append(meanCalcCadence(i))
    print(meanCadenceOfWorkouts)
    workoutsDf.insert(column = "Cadence", value = meanCadenceOfWorkouts, loc = 1)
    return workoutsDf

def addPowerToDataframe(dfs):
    meanPowerOfWorkouts = []
    for i in dfs:
        meanPowerOfWorkouts.append(meanCalcPower(i))
    print(meanPowerOfWorkouts)
    workoutsDf.insert(column = "Power", value = meanPowerOfWorkouts, loc = 1)
    return workoutsDf

def heartrateTo(workoutsDf):
    workoutsDf['heartrate'] = meanCalcHeartRate(workoutsDf["heart_rate"])
    return workoutsDf['heartrate']

#Alle im Directory befindlichen WorkoutIDs
workouts = importFiles(directory)
#Daraus ein Dataframe
workoutsDf = pd.DataFrame(data = workouts, columns= ["workoutID"])
#Import der Workoutdaten in dfFit
dfFit = getFitData(workouts)
df = formRelevantDataFrame(dfFit)

heart_rate = []
cadence = []
power = []
for i in dfFit:
    heart_rate.append(meanCalcHeartRate(i))
    cadence.append(meanCalcCadence(i))
    power.append(meanCalcPower(i))

print(heart_rate)
print(cadence)
print(power)


