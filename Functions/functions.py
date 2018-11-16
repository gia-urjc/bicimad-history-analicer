import json
from datetime import datetime, date

import dateutil.parser

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


def readStationInfo(filepath):
    with open(filepath) as f:
        stations_info = json.load(f)  # type: object

    stations = dict()
    for station in stations_info["stations"]:
        stations[int(station["id"])] = station
    return stations


def convertDictToList(dict):
    result = []
    for key, value in dict.iteritems():
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
