import pprint

import dateutil.parser
import os
import json
import sys
from Functions import functions
from StationsConfiguration.stations import Stations
from UserConfiguration.initialUsers import initialUsers
from UserConfiguration.userConfiguration import UserConfigurationObj
from pymongo import MongoClient
import datetime


# from GeoPosition import GeoPosition

# read the stations with latitude/longitude, capacity and ids

def generateUserConfiguration(stationsInfo):
    route_files = sys.argv[2] + "/"
    list_files = os.listdir(sys.argv[2])  # read the path of the routes files


    users = []

    for filename in list_files:
        if filename.endswith(".DS"):
            continue
        splitFile = filename.split("_")
        monthFile = splitFile[0][4:]
        yearFile = splitFile[0][0:4]
        if monthFile == "":
            continue
        monthFile = int(monthFile)
        yearFile = int(yearFile)

        if startDate.month >= monthFile >= endDate.month and startDate.year >= yearFile <= endDate.year:
            for line in open(route_files + filename):
                json_line = json.loads(line)
                if functions.isValidUser(json_line, startDate, endDate):
                    user = UserConfigurationObj(json_line["idunplug_station"], json_line["idplug_station"],
                                                {"typeName": "USER_COMMUTER", "parameters": {}},
                                                stationsInfo, json_line)
                    users.append(user)
            orderedUsers = sorted(users, key=lambda o: o.timeInstant)
            initialUsersWrite = initialUsers(orderedUsers)  # type: initialUsers
            with open("user_configuration.json", "w") as outfile:
                json.dump(initialUsersWrite, outfile, default=functions.jsonDefault, indent=4)


def generateStationConfiguration(date, stationsInfo):
    year = date[0]
    month = date[1]
    day = date[2]
    hour = date[3]
    minutes = date[4]
    seconds = date[5]

    client = MongoClient("localhost", 27017)
    db = client.mongo
    collection = db.generalInformation
    d_init = datetime.datetime(year, month, day, hour, minutes, seconds)
    d_end = datetime.datetime(year, month, day, hour, minutes + 5, seconds)
    for post in collection.find({"time": {"$gte": d_init, "$lte": d_end}}):
        if post:
            stations = post["data"]["stations"]
            stationsConfiguration = stationsInfo.copy()
            for station in stations:
                stationsConfiguration[station["_id"]]["bikes"] = station["dock_bikes"]
    stations = functions.convertDictToList(stationsConfiguration)
    stationsConfiguration = Stations(stations)
    with open("station_configuration.json", "w") as outfile:
        json.dump(stationsConfiguration, outfile, default=functions.jsonDefault, indent=4)


#MAIN functions called
startDate = dateutil.parser.parse(sys.argv[3])
endDate = dateutil.parser.parse(sys.argv[4])
stationsInfo = functions.readStationInfo(sys.argv[1])
#generateUserConfiguration(stationsInfo)
generateStationConfiguration([startDate.year, startDate.month, startDate.day,
                              startDate.hour, startDate.minute, startDate.second], stationsInfo)
print("termine")
