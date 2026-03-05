# This program will create and generate data based on rules in order to simulate data coming in from a source.
# Hours worked: 4 hour
# Author: Joshua Ngo


import random #For random number generation
import time #For timers and clock control
import threading #For multithreading sensors
from datetime import datetime #For timestamping

import asyncio
import websockets
import json

finalData = []
dataLock = threading.Lock()

#Class for a sensor object
#Name : Sensor's Name
#Data : Data in the form of a list (Might not be used)

class Sensor:
    def __init__(self, name, data, interval, minVal, maxVal, dataunit=None):
        self.name = name    #Sensor Name
        self.data = data    #Data array if needed later, this is currently unused. It is empty for each sensor created as of now.
        self.interval = interval    #The interval of the timer
        self.minVal = minVal
        self.maxVal = maxVal
        self.dataunit = dataunit    #Unit of data for this sensor
        self.running = False        #State of the sensor

    #Start the thread for this sensor
    def start(self):
        self.running = True     #Flag for running process
        self.thread = threading.Thread(target=self._generate)   #When a sensor starts up, it must start generating data right away.
        self.thread.start()     #Start the thread
        print("Sensor thread " + self.name + " is now running successfully")

    #Stop the thread for this sensor
    def stop(self):
        self.running = False #Flag for running process
        if self.thread:
            print("Sensor thread " + self.name + " has successfully stopped.")
        # self.thread.join()  #This is ensure that the thread exits properly, causes issues with stopping the program, so it is commented out for now.

    #Generate the data
    def _generate(self):
        while self.running:
            data = formatData(self) #Get a piece of data from the sensor
            with dataLock:  #Use the lock to make sure that this operation doesn't get race condition'd
                finalData.append(data)
            time.sleep(self.interval) #Halts the program in regards to the interval
            



#This function will generate fake data and sensors at a fast rate.
# variance : The value that will determine the variance in data for each random number generator
# Returns : randomized data value
def generateData(minVal, maxVal):
    # test = random.randrange(1,16336)    #Random number, does not include the endpoint
    # temp = (20 + random.random() * variance)
    # return temp

    value = random.uniform(minVal, maxVal)
    return value

#This function will start all the sensors
# sensorsList : The list of sensors to start
def startSensors(sensorsList):
    for sens in sensorsList:
        try:
            sens.start()    #Start all the sensors
        except:
            print("Error starting sensor.")

#This function will stop all the sensors.
# sensorsList : The list of sensors to stop
def stopSensors(sensorsList):
    for sens in sensorsList:
            sens.stop() #Stop all sensors

#This function will format the data from a sensor and return it in a printable format
#Note, in the GBTAC data, there is no unit involved. So, the unit parameter might not exist.
#Currently, it takes a sensor and prints its values.
#sensor : Sensor object
def formatData(sensor):
    #Set values 
    sensorData = sensor.data
    unit = sensor.dataunit
    name = sensor.name          #Sensor name
    running = sensor.running    #If the sensor is running
    interval = sensor.interval  #The interval in which the sensor should print data
    minVal = sensor.minVal
    maxVal = sensor.maxVal
    
    time = datetime.now()
    timestamp = time.strftime("%H:%M:%S")

    #String formatting
    nameHeader = f"Sensor Name: {name}"
    div = f"="*35

    #Start printing
    print(div)
    print(nameHeader)

    while running:  #This loop should only run when the sensors are running
        dataSample = generateData(minVal, maxVal)

        # data = (timestamp + " " + name + " " + str(dataSample))
        data = (name + "," + str(dataSample))

        print(data) #PUBLISH SINGLE HERE
        return data
        
        # time.sleep(interval) #Halts the program in regards to the interval
        # running = sensor.running #Update the thread's status 

#This function creates the sensors.
#Right now, sensorCount is not defined as it just makes however many sensors that are defined in the metrics_config array.
def createSensors(sensorCount, minVal, maxVal):

    arr = []

    metrics_config = [
        # Energy Consumption (kW)
        {"name": "GBT Total Consumption", "unit": "kW", "min": 250.0, "max": 500.0},
        {"name": "GBT Space heating", "unit": "kW", "min": 100.0, "max": 250.0},
        {"name": "GBT Lighting consumption-TL", "unit": "kW", "min": 20.0, "max": 80.0},

        # Energy Generation (kW)
        {"name": "GBT Total Generation", "unit": "kW", "min": 200.0, "max": 500.0},
        {"name": "PV-RooftopSolar_Total", "unit": "kW", "min": 100.0, "max": 300.0},
        {"name": "SaitSolarLab_20000_TL151", "unit": "kW", "min": 50.0, "max": 150.0},

        # Temperature Sensors (°C)
        {"name": "SLAB_Supply_Water_Temp_POLL", "unit": "°C", "min": 35.0, "max": 45.0},
        {"name": "HRV1_Supply_Temp_POLL", "unit": "°C", "min": 18.0, "max": 24.0},
        {"name": "HWS_Outside_Temp_POLL", "unit": "°C", "min": -10.0, "max": 15.0},
        {"name": "SLAB_Zn1_Basement_Avg_Space_Temp_AV_POLL", "unit": "°C", "min": 19.0, "max": 23.0},

        # HVAC Systems (Amps)
        {"name": "HRV1_SupFan_Amps_POLL", "unit": "A", "min": 2.0, "max": 6.0},
        {"name": "HRV2_SupFan_Amps_POLL", "unit": "A", "min": 2.0, "max": 6.0},
        {"name": "SLAB_P4A_Amps_POLL", "unit": "A", "min": 1.0, "max": 4.0},

        # Hot Water Systems (°C and Amps)
        {"name": "HWS_Post_DHW_Tank_Temp_POLL", "unit": "°C", "min": 55.0, "max": 65.0},
        {"name": "HWS_P1A_Amps_POLL", "unit": "A", "min": 0.5, "max": 2.5},
        {"name": "DHW_P5_Amps_POLL", "unit": "A", "min": 0.5, "max": 2.5},
    ]

    randInterval = random.randint(1,4)  #Generate a random interval for sensors for randomness

    for sensor in metrics_config:
        tempSens = Sensor(sensor["name"], [], randInterval, minVal, maxVal)
        arr.append(tempSens)

# Below is old stuff, keep this here and comment everything up above to get the old script working 
    # number = 0  #Sensor number
    # tl = 60 #Tl number
    # arr = []    #Array of sensors
    # for index in range(sensorCount):
    #     randInterval = random.randint(1,4)  #Generate a random interval for sensors for randomness
    #     tempSens = Sensor(sensorType + str(number) + "_30000_TL" + str(tl) , [] , randInterval, minVal, maxVal)
    #     arr.append(tempSens)
    #     number += 1
    #     tl += 1


    return arr #Array of sensors

#This function sends data to the client
#Websocket : the websocket that is connected
async def sendData(websocket):
    print(f"Client has connected. Sending data.")

    #Runs no matter what
    while True:
        with dataLock:  #Make sure lock the data
            await websocket.send(json.dumps(finalData))
            finalData.clear() #Clear the array, we don't want to send duplicate data.
        await asyncio.sleep(2)  #Sleep for two seconds, let the program run



#Main function
async def main():
    sensorsList = []    #List of all sensors

    solarSensors = createSensors(20,50.0,150.0)  #Create sensors with a label of SolarLab
    # tempSensors = createSensors(20, "TemperatureLabs")  #Create sensors with label of TemperatureLabs
    # occupancySensors = createSensors(25, "Occupancy")

    runTime = 20  #How long the program should run for

    #Combine the sensors into one large list
    sensorsList.extend(solarSensors)
    # sensorsList.extend(tempSensors)
    # sensorsList.extend(occupancySensors)

    #Function to start all the sensors
    startSensors(sensorsList)

    #This try-except clause is to help with program stoppage if needed.
    try:
        #Let the threads run while the main function sleeps for the runtime amount
        async with websockets.serve(sendData, "0.0.0.0", 9000):
            print("Server started. Awaiting connection.")
            await asyncio.sleep(runTime)
    except KeyboardInterrupt:   #If a keyboard interrupt is noticed, exit the entire program.
        print("\nForce stopping the program!\n")
    finally:    #Cleanup crew with function to stop all sensors
        with dataLock:
            stopSensors(sensorsList)
        # for i in finalData:
        #     print(i)


#Run the main function, which essentially handles the whole program
try:
    asyncio.run(main())
except KeyboardInterrupt:
    print("Server Stopping")    #Might not need this try except block, but is good practice


