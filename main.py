import dateutil.parser
import os
import json
import sys
from Functions import functions
from UserConfiguration.initialUsers import initialUsers
from UserConfiguration.userConfiguration import UserConfigurationObj
from pymongo import MongoClient
import datetime

# from GeoPosition import GeoPosition

# read the stations with latitude/longitude, capacity and ids
def jsonDefault(object):
    return object.__dict__


def generateUserConfiguration():
    route_files = sys.argv[2] + "/"
    route_stations_info = sys.argv[1] # path of the stations_info file
    list_files = os.listdir(sys.argv[2])  # read the path of the routes files
    startDate = dateutil.parser.parse(sys.argv[3])
    endDate = dateutil.parser.parse(sys.argv[4])

    users = []
    stationsInfo = functions.readStationInfo(route_stations_info)

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
            with open("prueba.json", "w") as outfile:
                json.dump(initialUsersWrite, outfile, default=jsonDefault, indent=4)

def generateStationConfiguration():
    client = MongoClient("localhost", 27017)
    db = client.mongo
    collection = db.generalInformation


generateUserConfiguration()
