# This program will create and generate data based on rules in order to simulate data coming in from a source.
# Hours worked: 4 hour
# Author: Joshua Ngo


import random #For random number generation
import time #For timers and clock control
import threading #For multithreading sensors

import asyncio
import websockets

finalData = []
dataLock = threading.Lock()

#Class for a sensor object
#Name : Sensor's Name
#Data : Data in the form of a list (Might not be used)

class Sensor:
    def __init__(self, name, data, interval, dataunit=None):
        self.name = name    #Sensor Name
        self.data = data    #Data array if needed later, this is currently unused. It is empty for each sensor created as of now.
        self.interval = interval    #The interval of the timer
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
def generateData(variance=7):
    # test = random.randrange(1,16336)    #Random number, does not include the endpoint
    temp = (20 + random.random() * variance)
    return temp

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

    #String formatting
    nameHeader = f"Sensor Name: {name}"
    div = f"="*35

    #Start printing
    print(div)
    print(nameHeader)

    while running:  #This loop should only run when the sensors are running
        dataSample = generateData()

        data = (name + " " + str(dataSample))
        print(data) #PUBLISH SINGLE HERE
        return data
        
        # time.sleep(interval) #Halts the program in regards to the interval
        # running = sensor.running #Update the thread's status 


def createSensors(sensorCount, sensorType,):
    number = 0  #Sensor number
    tl = 60 #Tl number
    arr = []    #Array of sensors
    for index in range(sensorCount):
        randInterval = random.randint(1,4)  #Generate a random interval for sensors for randomness
        tempSens = Sensor(sensorType + str(number) + "_30000_TL" + str(tl) , [] , randInterval)
        arr.append(tempSens)
        number += 1
        tl += 1
    return arr #Array of sensors

async def sendData(websocket):
    print(f"Client has connected. Sending data.")

    while True:
        with dataLock:
            await websocket.send("Hello world!")
        await asyncio.sleep(3)



#Main function
async def main():
    sensorsList = []    #List of all sensors

    solarSensors = createSensors(20,"SolarLab")  #Create sensors with a label of SolarLab
    # tempSensors = createSensors(20, "TemperatureLabs")  #Create sensors with label of TemperatureLabs
    # occupancySensors = createSensors(25, "Occupancy")

    runTime = 51  #How long the program should run for

    #Combine the sensors into one large list
    sensorsList.extend(solarSensors)
    # sensorsList.extend(tempSensors)
    # sensorsList.extend(occupancySensors)

    #Function to start all the sensors
    startSensors(sensorsList)

    # async with websockets.serve(sendData, "0.0.0.0", 9000):
    #     print("Server started. Awaiting connection.")
    #     await asyncio.Future()


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


