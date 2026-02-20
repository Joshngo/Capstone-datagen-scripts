#This script is a sample client that will be gathering data from the server.

import asyncio
import websockets
import json
import csv

async def main():

    allData = []    #Initialize the variable to hold all the data as it comes in
    async with websockets.connect("ws://localhost:9000") as websocket:  #Attempt to connect with the server
        await websocket.send("Hello Server!")   #Confirmation message

        # response = await websocket.recv()   #Wait for 

        #NOTE: This block of code could potentially cause problems if the information coming in is too large, if that happens, we will need to multithread this.
        try:
            while True:
                response = await websocket.recv()   #Wait for a response from the server, this will be the data
                data = json.loads(response)         #The data will be formatted back into array form
                print(data)                         #For debugging
                allData = allData + data
        except:
            print("Connection closed")  #This except clause is essential, because when the connection closes we don't want to throw and exception and break the program execution

    writeCsv(allData)   #Write all the data to the csv file

#This function will take an array of strings, (The Data) and write it to a csv file
#inputData : The array of strings (our data)
def writeCsv(inputData):
    copyData = inputData

    with open ("trend-log.csv", "w", newline="") as csvfile:    #Open the file as a csv
        writer = csv.writer(csvfile)
        writer.writerow(["timestamp", "name", "value"])

        #For each entry, we must split the strings by the spaces and extract the proper information
        for entry in copyData:
            splitStr = entry.split(" ")
            timestamp = splitStr[0]
            name = splitStr[1]
            value = splitStr[2]

            print(f"{timestamp} {name} {value}") #For debugging purposes

            writer.writerow([timestamp, name, value]) #Write the row to the csv file


asyncio.run(main())