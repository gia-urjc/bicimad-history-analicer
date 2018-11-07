import json
import dateutil.parser


def generateUser(self,user):
    json_line = json.loads(user)
    date = dateutil.parser.parse(json_line["unplug_hourTime"]["date"])

def isValidUser(user, startDate, endDate):
    date = dateutil.parser.parse(user["unplug_hourTime"]["date"])
    valid_time = 3*60
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
