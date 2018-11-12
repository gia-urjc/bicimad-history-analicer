import dateutil.parser

from GeoPosition.GeoPosition import GeoPosition
import random


def randomizeInstant(route):
    randomNumber = random.randint(0, 3600)
    date = dateutil.parser.parse(route["unplug_hourTime"]["date"])
    return randomNumber + (int(date.hour)*3600)


def getPositionByIdStation(idInit, stationsInfo):
    return GeoPosition(stationsInfo[idInit]["position"]["latitude"], stationsInfo[idInit]["position"]["longitude"])

def determinateVelocityAndDistance(route, idInit, idEnd, position, destinationPlace):
    if idInit != idEnd:
        if route.has_key("track"):
            track = route["track"]
            pointList = list()
            pointList.append(destinationPlace)
            for section in track["features"]:
                latitude = section["geometry"]["coordinates"][1]
                longitude = section["geometry"]["coordinates"][0]
                pointList.append(GeoPosition(latitude, longitude))
            pointList.append(position)
            distance = GeoPosition.calculateDistancesByList(pointList)
            velocity = distance / route["travel_time"]
            if velocity < 1:
                velocity = 4
            return distance, velocity
        else:
            distance = position.distanceTo(destinationPlace)
            velocity = distance / route["travel_time"]
            if velocity < 1:
                velocity = 4
            return distance, velocity
    else:
        if route.has_key("track"):
            track = route["track"]
            pointList = list()
            pointList.append(destinationPlace)
            for section in track["features"]:
                latitude = section["geometry"]["coordinates"][1]
                longitude = section["geometry"]["coordinates"][0]
                pointList.append(GeoPosition(latitude, longitude))
            pointList.append(position)
            distance = GeoPosition.calculateDistancesByList(pointList)
            velocity = distance / route["travel_time"]
            if velocity < 1:
                velocity = 4
            return distance, velocity
        else:
            velocity = 5
            distance = velocity * route["travel_time"]
            return distance, velocity


def randomizePosition(idStation, stationsInfo, distance):
    position = getPositionByIdStation(idStation, stationsInfo)
    return GeoPosition.randomPointCircle(position, distance)


def determinateIntermediatePosition(position, route, parameters, distance):
    intermediatePoint = GeoPosition.randomPointCircumference(position, distance/2)
    parameters["parameters"] = {"intermediatePosition": {"latitude": intermediatePoint.latitude,
                                                         "longitude": intermediatePoint.longitude}}
    return parameters


class UserConfigurationObj(object):

    def __init__(self, idInit, idEnd, parameters, stationsInfo, route):
        self.position = randomizePosition(idInit, stationsInfo, 200)
        self.destinationPlace = randomizePosition(idEnd, stationsInfo, 200)
        distance_velocity = determinateVelocityAndDistance(route, idInit, idEnd, self.position, self.destinationPlace)
        self.cyclingVelocity = distance_velocity[1]
        if idInit == idEnd:
            self.userType = determinateIntermediatePosition(self.position, route, parameters, distance_velocity[0])
        else:
            self.userType = parameters
        self.idInitialStation = idInit
        self.idEndStation = idEnd
        self.timeInstant = randomizeInstant(route)
