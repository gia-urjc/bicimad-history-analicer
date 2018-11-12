import dateutil.parser
import os
import json
import sys

from Commons.constants import NUM_STATIONS
from Functions import functions
import Matrix_module
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
            initialUsersWrite = initialUsers(orderedUsers)
            with open("user_configuration.json", "w") as outfile:
                json.dump(initialUsersWrite, outfile, default=functions.jsonDefault, indent=4)


def generateStationConfiguration(date, stationsInfo):
    year = date[0]
    month = date[1]
    day = date[2]
    hour = date[3]
    minutes = date[4]
    seconds = date[5]
    count_bikes = 0

    client = MongoClient("localhost", 27017)
    db = client.mongo
    collection = db.generalInformation
    d_init = datetime.datetime(year, month, day, hour, minutes, seconds)
    d_end = datetime.datetime(year, month, day, hour, minutes + 5, seconds)
    for post in collection.find({"time": {"$gte": d_init, "$lte": d_end}}):
        if post:
            stations = post["data"]['stations']
            stationsConfiguration = stationsInfo.copy()
            for station in stations:
                stationsConfiguration[station["_id"]]["bikes"] = station["dock_bikes"]
                count_bikes += int(stationsConfiguration[station["_id"]]["bikes"])
    stations = functions.convertDictToList(stationsConfiguration)
    stationsConfiguration = Stations(stations)
    stationsConfiguration.comprobar()
    for i in range(0, 173):

        stationsConfiguration.stations[i]["bikes"] = stationsConfiguration.stations[i]["capacity"] / 2
    with open("station_configuration.json", "w") as outfile:
        json.dump(stationsConfiguration, outfile, default=functions.jsonDefault, indent=4)


def generateDemandMatrix(startDate, endDate, stationsInfo):
    """

    :param startate: initial date to start the analitic
    :param endDate: final date to start the analitic
    :param stationsInfo: object with the state of the stations on the system
    :return: DemandMatrix object
    """
    # auxiliar variables
    demandMatrixWeek = Matrix_module.DemandMatrix()
    demandMatrixWeekend = Matrix_module.DemandMatrix()
    counterDaysWeek = 0
    counterDaysWeekend = 0
    counterRegister_R = 0
    datesMapWeek = dict()
    datesMapWeekend = dict()
    list_files = os.listdir(sys.argv[2])  # read the path of the routes files
    route_files = sys.argv[2] + "/"

    for filename in list_files:
        if filename.endswith(".DS_Store"):
            continue
        splitFile = filename.split("_")
        monthFile = splitFile[0][4:]
        yearFile = splitFile[0][0:4]
        if monthFile == "":
            continue
        monthFile = int(monthFile)
        yearFile = int(yearFile)

        if startDate.month <= monthFile <= endDate.month and startDate.year <= yearFile <= endDate.year:
            for line in open(route_files + filename):
                json_line = json.loads(line)
                date = dateutil.parser.parse(json_line["unplug_hourTime"]["date"])
                if functions.isValidUser(json_line, startDate, endDate):
                    counterRegister_R += 1
                    if functions.isWeekend(date):
                        if not datesMapWeekend.get(date.date()):
                            datesMapWeekend.setdefault(date.date(), True)
                            counterDaysWeekend += 1
                        demandMatrixWeekend.addValue(json_line, NUM_STATIONS)

                    else:
                        if not datesMapWeek.get(date.date()):
                            datesMapWeek.setdefault(date.date(), True)
                            counterDaysWeek += 1
                        demandMatrixWeek.addValue(json_line, NUM_STATIONS)

    #Remove register with station id=0
    for i in range(0, NUM_STATIONS):
        demandMatrixWeek.matrices[i].pop(0)
        demandMatrixWeekend.matrices[i].pop(0)
    demandMatrixWeekend.matrices.pop(0)
    demandMatrixWeek.matrices.pop(0)
    result = Matrix_module.MatricesInfo(demandMatrixWeek, demandMatrixWeekend)
    result.addCounters(counterDaysWeek, counterDaysWeekend, counterRegister_R)
    with open("demandMatrix.json", "w") as outfile:
        json.dump(result, outfile, default=functions.jsonDefault, indent=4)
    return result

def analyticsData():
    if sys.argv[5]:
        if os.path.isfile(sys.argv[5]):
            with open(sys.argv[5]) as filename:
                aux = json.load(filename)
                week = Matrix_module.DemandMatrix()
                weekend = Matrix_module.DemandMatrix()
                week.matrices = aux["matrix_week"]["matrices"]
                weekend.matrices = aux["matrix_weekend"]["matrices"]
                demand_matrices = Matrix_module.MatricesInfo(week, weekend)
                demand_matrices.addCounters(aux["counter_days_week"], aux["counter_days_weekend"],
                                            aux["counter_register_r"])

        else:
            demand_matrices = generateDemandMatrix(startDate, endDate, stationsInfo)
    else:
        demand_matrices = generateDemandMatrix(startDate, endDate, stationsInfo)

    return demand_matrices


# MAIN functions called
startDate = dateutil.parser.parse(sys.argv[3])
endDate = dateutil.parser.parse(sys.argv[4])
stationsInfo = functions.readStationInfo(sys.argv[1])
#generateUserConfiguration(stationsInfo)
generateStationConfiguration([startDate.year, startDate.month, startDate.day,
                             startDate.hour, startDate.minute, startDate.second], stationsInfo)

#demandMatrices = analyticsData()
#averageMatrices = demandMatrices.generateAverageMatrices()  # type: MatricesInfo
#averageArray = averageMatrices.arrayAverage()
#usersInstant = demandMatrices.matrixUsersStationByInstant()
#probability = demandMatrices.generateProbabilityMatrix(usersInstant)
#functions.writeFile(usersInstant, "matrixUsersStationByInstant.json")
#functions.writeFile(averageMatrices, "averageMatrix.json")
#functions.writeFile(probability, "probabilityMatrix.json")


print("termine")
