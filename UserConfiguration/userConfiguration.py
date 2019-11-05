import dateutil.parser

from GeoPosition.GeoPosition import GeoPosition
import random


def randomizeInstant(route):
    randomNumber = random.randint(0, 3600)
    date = dateutil.parser.parse(route["unplug_hourTime"]["date"])
    return randomNumber + (int(date.hour)*3600)

def randomizeInstant2(route):
    randomNumber = random.randint(0, 3600)
    date = dateutil.parser.parse(route["unplug_hourTime"])
    return randomNumber + (int(date.hour)*3600)

def exactTime(route, startDate):
    # type: (object) -> object
    date = dateutil.parser.parse(route["unplug_hourTime"])
    startDate = int(startDate.minute*60) + int(startDate.hour*3600)
    return (int(date.minute)*60) + (int(date.hour)*3600) - startDate

def getPositionByIdStation(idInit, stationsInfo):
    return GeoPosition(stationsInfo[idInit]["position"]["latitude"], stationsInfo[idInit]["position"]["longitude"])

def determinateVelocityAndDistance(route, idInit, idEnd, position, destinationPlace):
    if idInit != idEnd:
        """if "track" in route:
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
            return distance, velocity"""

        distance = position.distanceTo(destinationPlace)
        velocity = distance / route["travel_time"]
        if velocity < 1:
            velocity = 4
        return distance, velocity
    else:
        '''if "track" in route:
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
            return distance, velocity'''
        velocity = 5
        distance = velocity * route["travel_time"]
        return distance, velocity


def randomizePosition(idStation, stationsInfo, distance):
    position = getPositionByIdStation(idStation, stationsInfo)
    return position
    #GeoPosition.randomPointCircle(position, distance)


def determinateIntermediatePosition(position, parameters, distance):
    intermediatePoint = GeoPosition.randomPointCircumference(position, distance/2)
    parameters["parameters"] = {"intermediatePosition": {"latitude": intermediatePoint.latitude,
                                                         "longitude": intermediatePoint.longitude}}
    return parameters


class UserConfigurationObj(object):

    def __init__(self, idInit, idEnd, parameters, travelTime, stationsInfo, route, selected=0, startDate=0, specialUser=False):
        self.position = randomizePosition(idInit, stationsInfo, 200)
        self.destinationPlace = randomizePosition(idEnd, stationsInfo, 200)
        distance_velocity = determinateVelocityAndDistance(route, idInit, idEnd, self.position, self.destinationPlace)
        self.cyclingVelocity = distance_velocity[1]
        self.travelTime = travelTime
        if not specialUser:
            if idInit == idEnd:
                self.userType = determinateIntermediatePosition(self.position, parameters, distance_velocity[0])
            else:
                self.userType = parameters
        else:
            self.userType = parameters
        self.idInitialStation = idInit
        self.idEndStation = idEnd
        if selected == 0:
            self.timeInstant = randomizeInstant(route)
        elif selected == 1:
            self.timeInstant = randomizeInstant2(route)
        else:
            self.timeInstant = exactTime(route, startDate)
