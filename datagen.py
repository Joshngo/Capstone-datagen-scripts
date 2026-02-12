# This program will create and generate data based on rules in order to simulate data coming in from a source.
# Hours worked: 4 hour
# Author: Joshua Ngo


import random #For random number generation
import time #For timers and clock control
import threading #For multithreading sensors

#Class for a sensor object
#Name : Sensor's Name
#Data : Data in the form of a list (Might not be used)

class Sensor:
    def __init__(self, name, data, interval, dataunit=None):
        self.name = name    #Sensor Name
        self.data = data    #Data array if needed later
        self.interval = interval    #The interval of the timer
        self.dataunit = dataunit    #Unit of data for this sensor
        self.running = False        #State of the sensor

    #Start the thread for this sensor
    def start(self):
        self.running = True     #Flag for running process
        self.thread = threading.Thread(target=self._generate)
        self.thread.start()     #Start the thread
        print("Sensor thread " + self.name + " is now running successfully")

    #Stop the thread for this sensor
    def stop(self):
        self.running = False #Flag for running process
        if self.thread:
            # self.thread.join()  #This is ensure that the thread exits properly
            print("Sensor thread " + self.name + " has successfully stopped.")

    #Generate the data
    def _generate(self):
        while self.running:
            formatData(self)



#This function will generate fake data and sensors at a fast rate.
#Returns : 
def generateData():
    # test = random.randrange(1,16336)    #Random number, does not include the endpoint
    temp = (20 + random.random() * 7)
    return temp


#This function will format the data from a sensor and return it in a printable format
#Note, in the GBTAC data, there is no unit involved. So, the unit parameter might not exist.
#Currently, it takes a sensor and prints its values.
#sensor : Sensor object
def formatData(sensor):
    #Set values 
    sensorData = sensor.data
    unit = sensor.dataunit
    name = sensor.name
    running = sensor.running
    interval = sensor.interval

    nameHeader = f"Sensor Name: {name}"
    div = f"="*35

    #Start printing
    print(div)
    print(nameHeader)

    while running:
        running = sensor.running
        dataSample = generateData()

        print(name + " " + str(dataSample)) #PUBLISH SINGLE HERE
        
        time.sleep(interval)
    
    print(div+"\n")


#Hard coded sensors
sens1 = Sensor("SolarLab1_30000_TL60" , [] , 1 , "")
sens2 = Sensor("SolarLab2_30000_TL61" , [] , 2 , "")
sens3 = Sensor("SolarLab3_30000_TL63" , [] , 3 , "")
sens4 = Sensor("TempLab4_30000_TL67", [] , 4 , "Celsius" )


energySensors = []

occupancySensors = []

#TODO: Change the interval for sensors. Just change the interval value every few sensors

def createSensors(sensorCount, sensorType,):
    number = 0
    tl = 60
    arr = []
    for index in range(sensorCount):
        tempSens = Sensor("SolarLab" + str(number) + "_30000_TL" + str(tl) , [] , 4)
        arr.append(tempSens)
        number += 1
        tl += 1
    return arr #Array of sensors



#Main function
def main():

    tempSensors = createSensors(25,"Temp")
    runTime = 20

    for sens in tempSensors:
        sens.start()

    time.sleep(runTime)

    for sens in tempSensors:
        sens.stop()

    # sens1.start()
    # sens2.start()
    # sens3.start()
    # time.sleep(runTime)
    # sens1.stop()
    # sens2.stop()
    # sens3.stop()

main()

