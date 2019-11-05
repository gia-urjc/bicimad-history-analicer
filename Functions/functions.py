import json
import sys

import dateutil.parser

from StationsConfiguration.stations import Stations
from TimeSeriesData.ArrayTimeSeries import ArrayTimeSeries
from TimeSeriesData.timeSeriesData import TimeSeriesData


def generateUser(self, user):
    json_line = json.loads(user)
    date = dateutil.parser.parse(json_line["unplug_hourTime"]["date"])


def isValidUser(user, startDate, endDate):
    date = dateutil.parser.parse(user["unplug_hourTime"]["date"])
    valid_time = 3 * 60
    user_type = user["user_type"]
    valid = startDate <= date <= endDate and user["travel_time"] >= valid_time and user_type != 3
    return valid

def isValidUserType3(user, startDate, endDate):
    date = dateutil.parser.parse(user["unplug_hourTime"]["date"])
    user_type = user["user_type"]
    valid = startDate <= date <= endDate and user_type == 3
    return valid

def isValidUserLondon(user, startDate, endDate):
    valid_stations = [175, 463, 482, 795, 8, 284, 145, 659, 672, 311, 20, 827, 153, 175, 826]
    date = dateutil.parser.parse(user["unplug_hourTime"], dayfirst=True)
    id_init = user["idunplug_station"]
    id_end = user["idplug_station"]
    valid_time = 3 * 60
    valid = ((startDate <= date <= endDate) and (user["travel_time"] >= valid_time)
             and (id_init not in valid_stations) and (id_end not in valid_stations))
    return valid

def isValidUserNY(user, startDate, endDate):
    valid_stations = [453]
    date = dateutil.parser.parse(user["unplug_hourTime"], dayfirst=True)
    id_init = user["idunplug_station"]
    id_end = user["idplug_station"]
    valid_time = 3 * 60
    valid = ((startDate <= date <= endDate) and (user["travel_time"] >= valid_time)
             and (id_init not in valid_stations) and (id_end not in valid_stations))
    return valid

def readStationInfo(filepath):
    with open(filepath) as f:
        stations_info = json.load(f)  # type: object

    stations = dict()
    for station in stations_info["stations"]:
        stations[int(station["id"])] = station
    return stations


def convertDictToList(dict):
    result = []
    for key, value in dict.items():
        temp = [key, value]
        result.append(temp[1])
    return result


def jsonDefault(object):
    return object.__dict__


def isWeekend(date):
    return date.isoweekday() == 6 or date.isoweekday() == 7


def writeFile(objet_to_write, name_file):
    with open(name_file, "w") as outfile:
        json.dump(objet_to_write, outfile, default=jsonDefault, indent=4)


def existRegister(data, date, id):
    result = False
    for x in data:
        if x.__date == date and x.__id == id:
            result = True
    return result


def generateTimeSeriesData(filename):
    result_unplug = dict()
    result_plug = dict()
    for line in open(filename):
        json_line = json.loads(line)
        dateRegister = dateutil.parser.parse(json_line["unplug_hourTime"]["date"])
        idStation_unplug = json_line["idunplug_station"]
        idStation_plug = json_line["idplug_station"]
        key_unplug = dateRegister, idStation_unplug
        key_plug = dateRegister, idStation_plug
        if key_unplug in result_unplug:
            # sumar 1 al amount de este registro
            result_unplug[key_unplug].amount += 1
        else:
            # crear un nuevo registro para esta fecha
            aux = TimeSeriesData(idStation_unplug, dateRegister.strftime('%Y/%m/%d %H:%M:%S'), 1)  # type: TimeSeriesData
            result_unplug[key_unplug] = aux
        if key_plug in result_plug:
            # sumar 1 al amount de este registro
            result_plug[key_plug].amount += 1
        else:
            # crear un nuevo registro para esta fecha
            aux = TimeSeriesData(idStation_plug, dateRegister.strftime('%Y/%m/%d %H:%M:%S'), 1)  # type: TimeSeriesData
            result_plug[key_plug] = aux

    return result_unplug, result_plug

def listDaysMinUsersBicimad(min_users, list_files):
    list_days = dict()
    result = []
    max_day = dict()
    for filename in list_files:
        if filename.endswith(".DS_Store"):
            continue

        route_files = sys.argv[2] + "/"
        for line in open(route_files + filename):
            json_line = json.loads(line)
            date = dateutil.parser.parse(json_line["unplug_hourTime"]["date"]) #Bicimad
            #date = dateutil.parser.parse(json_line["unplug_hourTime"])#Londres-NY
            date_key = date.date()
            if date_key in list_days:
                list_days[date_key] += 1
            else:
                list_days[date_key] = 1
        for key, value in list_days.items():
            if list_days[key] > min_users:
                result.append(list_days[key])

    return list_days

def generateStationLondonConfiguration(station_info):
    # type: (object) -> object
    stations_valid = []
    for station in station_info.values():
        x = {"position": station["position"], "bikes": station["bikes"]*2, "capacity": station["capacity"]*2,
             "id": station["id"]}
        #x = {"position": station["position"], "bikes": 500, "capacity": 1000,
        #     "id": station["id"]}
        stations_valid.append(x)
        stationsConfiguration = Stations(stations_valid)
    writeFile(stationsConfiguration, "stations_configuration.json")

def countTotalBikesLondon(station_info):
    count_bikes = 0
    count_docks = 0
    for station in station_info.values():
        count_bikes += station["bikes"]
        count_docks += station["capacity"]
    print("Total number of bikes: " + str(count_bikes))
    print("Total number of docks: " + str(count_docks))