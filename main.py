# coding=utf-8
import dateutil.parser
import os
import json
import sys
import random

from Commons.constants import NUM_STATIONS
from Functions import functions
import Matrix_module
from StationsConfiguration.stations import Stations
from TimeSeriesData.ArrayTimeSeries import ArrayTimeSeries
from UserConfiguration.initialUsers import initialUsers
from UserConfiguration.userConfiguration import UserConfigurationObj
from pymongo import MongoClient
import datetime


# from GeoPosition import GeoPosition

# read the stations with latitude/longitude, capacity and ids

def generateUserConfigurationBicimad(stationsInfo):
    route_files = sys.argv[2] + "/"
    list_files = os.listdir(sys.argv[2])  # read the path of the routes files
    count_users_informed = 0
    count_users_obedient = 0
    users = []

    for filename in list_files:
        if filename.endswith(".DS_Store"):
            continue
        splitFile = filename.split("_")
        monthFile = splitFile[0][4:6]
        yearFile = splitFile[0][0:4]
        if monthFile == "":
            continue
        monthFile = int(monthFile)
        yearFile = int(yearFile)

        if startDate.month >= monthFile >= endDate.month and startDate.year >= yearFile >= endDate.year:
            for line in open(route_files + filename):
                if line[0] != "{":
                    continue
                if line[len(line) - 2] == ",":
                    line = line[0:len(line) - 2]
                json_line = json.loads(line)
                if functions.isValidUser(json_line, startDate, endDate):
                    x = random.randint(0, 1)
                    if x < 1:
                        user_processed = UserConfigurationObj(json_line["idunplug_station"],
                                                              json_line["idplug_station"],
                                                              {"typeName": "USER_PAPERAT2018_INF", "parameters": {}},
                                                              json_line["travel_time"],
                                                              stationsInfo, json_line)
                        count_users_informed += 1
                    else:
                        user_processed = UserConfigurationObj(json_line["idunplug_station"],
                                                              json_line["idplug_station"],
                                                              {"typeName": "USER_PAPERAT2018_OBHOLGER", "parameters": {}},
                                                              json_line["travel_time"],
                                                              stationsInfo, json_line)
                        count_users_obedient += 1
                    users.append(user_processed)
            orderedUsers = sorted(users, key=lambda o: o.timeInstant)
            initialUsersWrite = initialUsers(orderedUsers)
            with open("users_configuration.json", "w") as outfile:
                json.dump(initialUsersWrite, outfile, default=functions.jsonDefault, indent=4)
    print("informados" + str(count_users_informed))
    print("obedientes" + str(count_users_obedient))


def resumeTrackRoute(initialUsers):
    resume = list()
    #recorrer diccionario de usuarios para sacar un resumen de estos
    resume_user = {"idInitialStation": initialUsers[0].idInitialStation, "idEndStation": initialUsers[0].idEndStation,
                   "num_bikes": 0, "travelTime": initialUsers[0].travelTime}
    for user in initialUsers:
        if (user.idInitialStation == resume_user["idInitialStation"]) and (user.idEndStation == resume_user["idEndStation"]):
            resume_user["num_bikes"] += 1
            if user.travelTime < resume_user["travelTime"]:
                resume_user["travelTime"] = user.travelTime
        else:
            resume.append(resume_user)
            resume_user = {"idInitialStation": user.idInitialStation, "idEndStation": user.idEndStation,
                           "num_bikes": 1, "travelTime": user.travelTime}
    with open("users_track_resume.json", "w") as outfile:
        json.dump(resume, outfile,  indent=4)
    pass

def reaconditionTimeInstants(initialUsers):
    resume_user = {"idInitialStation": initialUsers[0].idInitialStation, "idEndStation": initialUsers[0].idEndStation,
                   "travelTime": initialUsers[0].travelTime, "timeInstant": initialUsers[0].timeInstant}
    initialUsers.pop(0)
    for user in initialUsers:
        if (user.idInitialStation == resume_user["idInitialStation"]) and (user.idEndStation == resume_user["idEndStation"]):
            auxTime = int((user.travelTime - resume_user["travelTime"]) / 2)
            user.timeInstant = resume_user["timeInstant"] + auxTime
        else:
            resume_user = {"idInitialStation": user.idInitialStation, "idEndStation": user.idEndStation,
                           "travelTime": user.travelTime, "timeInstant": user.timeInstant}
    return initialUsers


def generateUserConfigurationType3(stationsInfo):
    route_files = sys.argv[2] + "/"
    list_files = os.listdir(sys.argv[2])  # read the path of the routes files
    count_users_informed = 0
    count_users_obedient = 0
    users = []

    for filename in list_files:
        if filename.endswith(".DS_Store"):
            continue
        splitFile = filename.split("_")
        monthFile = splitFile[0][4:6]
        yearFile = splitFile[0][0:4]
        if monthFile == "":
            continue
        monthFile = int(monthFile)
        yearFile = int(yearFile)

        if startDate.month >= monthFile >= endDate.month and startDate.year >= yearFile >= endDate.year:
            for line in open(route_files + filename):
                if line[0] != "{":
                    continue
                if line[len(line) - 2] == ",":
                    line = line[0:len(line) - 2]
                json_line = json.loads(line)
                if functions.isValidUserType3(json_line, startDate, endDate):
                    user_processed = UserConfigurationObj(json_line["idunplug_station"],
                                                              json_line["idplug_station"],
                                                              {"typeName": "USER_TRACK", "parameters": {}},
                                                              json_line["travel_time"],
                                                              stationsInfo, json_line)

                    users.append(user_processed)
            orderedUsers = sorted(users, key=lambda o: o.idInitialStation)
            #funcion para sacar el resumen de los usuarios de camiones y escribir un resumen con este
            resumeTrackRoute(orderedUsers)
            orderedUsers = reaconditionTimeInstants(orderedUsers)
            initialUsersWrite = initialUsers(orderedUsers)
            with open("users_configurationType3.json", "w") as outfile:
                json.dump(initialUsersWrite, outfile, default=functions.jsonDefault, indent=4)

def generateUserConfigurationNY(stationsInfo):
    route_files = sys.argv[2] + "/"
    list_files = os.listdir(sys.argv[2])  # read the path of the routes files
    count_users_informed = 0
    count_users_obedient = 0
    users = []

    for filename in list_files:
        if filename.endswith(".DS_Store"):
            continue
        splitFile = filename.split("_")
        monthFile = splitFile[0][4:6]
        yearFile = splitFile[0][0:4]
        if monthFile == "":
            continue
        monthFile = int(monthFile)
        yearFile = int(yearFile)

        if startDate.month >= monthFile >= endDate.month and startDate.year >= yearFile <= endDate.year:
            for line in open(route_files + filename):
                if line[0] != "{":
                    continue
                if line[len(line) - 2] == ",":
                    line = line[0:len(line) - 2]
                json_line = json.loads(line)
                if functions.isValidUserNY(json_line, startDate, endDate):
                    x = random.randint(0, 1)
                    if x < 1:
                        user_processed = UserConfigurationObj(json_line["idunplug_station"],
                                                              json_line["idplug_station"],
                                                              {"typeName": "USER_PAPERAT2018_INF", "parameters": {}},
                                                              stationsInfo, json_line, 2)
                        count_users_informed += 1
                    else:
                        user_processed = UserConfigurationObj(json_line["idunplug_station"],
                                                              json_line["idplug_station"],
                                                              {"typeName": "USER_PAPERAT2018_OBHOLGER",
                                                               "parameters": {}},
                                                              stationsInfo, json_line, 2)
                        count_users_obedient += 1
                    users.append(user_processed)
            orderedUsers = sorted(users, key=lambda o: o.timeInstant)
            initialUsersWrite = initialUsers(orderedUsers)
            with open("users_configuration.json", "w") as outfile:
                json.dump(initialUsersWrite, outfile, default=functions.jsonDefault, indent=4)
    print("informados" + str(count_users_informed))
    print("obedientes" + str(count_users_obedient))


def generateUserConfigurationLondon(stationsInfo):
    route_files = sys.argv[2] + "/"
    list_files = os.listdir(sys.argv[2])  # read the path of the routes files
    count_users_informed = 0
    count_users_obedient = 0
    users = []

    for filename in list_files:
        if filename.endswith(".DS_Store"):
            continue
        splitFile = filename.split("_")
        monthFile = splitFile[0][4:6]
        yearFile = splitFile[0][0:4]
        if monthFile == "":
            continue
        monthFile = int(monthFile)
        yearFile = int(yearFile)

        if startDate.month >= monthFile >= endDate.month and startDate.year >= yearFile <= endDate.year:
            for line in open(route_files + filename):
                if line[0] != "{":
                    continue
                if line[len(line) - 2] == ",":
                    line = line[0:len(line) - 2]
                json_line = json.loads(line)
                if functions.isValidUserLondon(json_line, startDate, endDate):
                    # x = random.randint(0, 1)
                    x = 0
                    if x < 1:
                        user_processed = UserConfigurationObj(json_line["idunplug_station"],
                                                              json_line["idplug_station"],
                                                              {"typeName": "USER_PAPERAT2018_INF", "parameters": {}},
                                                              stationsInfo, json_line, 2, startDate)
                        count_users_informed += 1
                    else:
                        user_processed = UserConfigurationObj(json_line["idunplug_station"],
                                                              json_line["idplug_station"],
                                                              {"typeName": "USER_PAPERAT2018_OBHOLGER",
                                                               "parameters": {}},
                                                              stationsInfo, json_line, 2, startDate)
                        count_users_obedient += 1
                    users.append(user_processed)
            orderedUsers = sorted(users, key=lambda o: o.timeInstant)
            initialUsersWrite = initialUsers(orderedUsers)
            with open("users_configuration.json", "w") as outfile:
                json.dump(initialUsersWrite, outfile, default=functions.jsonDefault, indent=4)
    print("informados" + str(count_users_informed))
    print("obedientes" + str(count_users_obedient))


def generateStationConfiguration(date, stationsInfo, halfStations=False):
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
    #for i in range(0, 173):
    #    if halfStations:
    #        stationsConfiguration.stations[i]["capacity"] = stationsConfiguration.stations[i]["capacity"] / 2
    #    stationsConfiguration.stations[i]["bikes"] = stationsConfiguration.stations[i]["capacity"] / 2
    with open("stations_configuration.json", "w") as outfile:
        json.dump(stationsConfiguration, outfile, default=functions.jsonDefault, indent=4)
    outfile.close()


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
                if line[0] != "{":
                    continue
                if line[len(line) - 2] == ",":
                    line = line[0:len(line) - 2]
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

    # Remove register with station id=0
    for i in range(0, NUM_STATIONS):
        demandMatrixWeek.matrices[i].pop(0)
        demandMatrixWeekend.matrices[i].pop(0)
    demandMatrixWeekend.matrices.pop(0)
    demandMatrixWeek.matrices.pop(0)
    result = Matrix_module.MatricesInfo(demandMatrixWeek, demandMatrixWeekend)
    result.addCounters(counterDaysWeek, counterDaysWeekend, counterRegister_R)
    with open("results/demandMatrix.json", "w") as outfile:
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


def generateDataTimeSeries():
    # auxiliar variables
    list_files = os.listdir(sys.argv[2])  # read the path of the routes files

    for filename in list_files:
        if filename.endswith(".DS_Store"):
            continue
        splitFile = filename.split("_")
        route_files = sys.argv[2] + "/"
        result = functions.generateTimeSeriesData(route_files + filename)
        returnValue_unplug = ArrayTimeSeries()
        returnValue_plug = ArrayTimeSeries()
        for item in result[0].values():
            returnValue_unplug.array.append(item)
        splitFile = filename.split("_")
        functions.writeFile(returnValue_unplug, "results/" + splitFile[0] + "_unplug_TS.json")
        for item in result[1].values():
            returnValue_plug.array.append(item)
        splitFile = filename.split("_")
        functions.writeFile(returnValue_plug, "results/" + splitFile[0] + "_plug_TS.json")
    return None


def main():
    print("escoja una opción del menú, introduzca el número de la lista que desee ejecutar:\n"
          "     1) Crear configuracion de usuarios de Bicimad (1)\n"
          "     2) Crear configuración de usuarios de Londres (2)\n"
          "     3) Crear configuración de usuaruos de New York (3)\n"
          "     4) Crear configuración de estaciones (4)\n"
          "     5) Ejecutar y crear ficheros de matrices de demanda del sistema BiciMad (5)\n"
          "     6) Crear configuracion de usuarios de Bicimad del tipo=3\n"
          )
    elem = int(sys.stdin.read())
    if (elem == 0):
        sys.exit(200)
    if (elem == 1):
        generateUserConfigurationBicimad(stationsInfo)
        sys.exit(200)
    elif (elem == 2):
        generateUserConfigurationLondon(stationsInfo)
        sys.exit(200)
    elif elem == 3:
        generateUserConfigurationNY(stationsInfo)
        sys.exit(200)
    elif elem == 4:
        generateStationConfiguration([startDate.year, startDate.month, startDate.day,
                                      startDate.hour, startDate.minute, startDate.second], stationsInfo)
        sys.exit(200)
    elif 5 == elem:
        demandMatrices = analyticsData()
        averageMatrices = demandMatrices.generateAverageMatrices()  # type: MatricesInfo
        averageArray = averageMatrices.arrayAverage()
        usersInstant = demandMatrices.matrixUsersStationByInstant()
        probability = demandMatrices.generateProbabilityMatrix(usersInstant[0])
        functions.writeFile(usersInstant[0], "results/matrixUsersStationByInstant_unplug.json")
        functions.writeFile(usersInstant[1], "results/matrixUsersStationByInstant_plug.json")
        functions.writeFile(averageMatrices, "results/averageMatrix.json")
        functions.writeFile(probability, "results/probabilityMatrix.json")
        sys.exit(200)
    elif 6 == elem:
        generateUserConfigurationType3(stationsInfo)
        sys.exit(200)
    else:
        main()


# MAIN functions called
startDate = dateutil.parser.parse(sys.argv[3])
endDate = dateutil.parser.parse(sys.argv[4])
stationsInfo = functions.readStationInfo(sys.argv[1])
# functions.generateStationLondonConfiguration(stationsInfo)
# functions.countTotalBikesLondon(stationsInfo)
main()
# x = functions.listDaysMinUsersBicimad(20000, os.listdir(sys.argv[2]))
# print x
# generateDataTimeSeries()
#
