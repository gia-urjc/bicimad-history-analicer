import math
import random
from Commons.constants import EARTH_RADIUS


class GeoPosition(object):

    def __init__(self, latitude, longitude):
        self.latitude = latitude
        self.longitude = longitude

    def distanceTo(self, point):
        f = [math.radians(self.latitude), math.radians(point.latitude)]
        l = [math.radians(self.longitude), math.radians(point.longitude)]
        h = self.haversine(f[1] - f[0]) + math.cos(f[0]) * math.cos(f[1]) * self.haversine(l[1] - l[0])
        return 2 * EARTH_RADIUS * math.asin(math.sqrt(h))

    def haversine(self, value):
        return math.pow(math.sin(value / 2), 2)

    @classmethod
    def randomPointCircle(cls, origin, radius):
        # type: (object, object) -> object
        rangeMin = 0
        rangeMax = radius
        DEGREES_TO_RADIANS = math.pi / 180.0

        randomNumbers = random.random()
        latitudeRadians = origin.latitude * DEGREES_TO_RADIANS
        longitudeRadians = origin.longitude * DEGREES_TO_RADIANS
        senLatitude = math.sin(latitudeRadians)
        cosLatitude = math.cos(latitudeRadians)

        # Random angle
        bearing = random.random() * 2 * math.pi
        randomValue = rangeMin + (rangeMax - rangeMin) * random.random()
        delta = (radius - randomValue) / EARTH_RADIUS
        senBearing = math.sin(bearing)
        cosBearing = math.cos(bearing)
        senDelta = math.sin(delta)
        cosDelta = math.cos(delta)
        resLatRadians = math.asin(senLatitude * cosDelta + cosLatitude * senDelta * cosBearing)
        resLonRadians = longitudeRadians + math.atan2(senBearing * senDelta * cosLatitude,
                                                      cosDelta - senLatitude * math.sin(resLatRadians))
        resLonRadians = ((resLonRadians + (math.pi * 3)) % (math.pi * 2)) - math.pi

        resLatitude = resLatRadians / DEGREES_TO_RADIANS
        resLongitude = resLonRadians / DEGREES_TO_RADIANS

        return GeoPosition(resLatitude, resLongitude)

    @classmethod
    def randomPointCircumference(cls, origin, radius):
        DEGREES_TO_RADIANS = math.pi / 180.0

        randomNumbers = random.random()
        latitudeRadians = origin.latitude * DEGREES_TO_RADIANS
        longitudeRadians = origin.longitude * DEGREES_TO_RADIANS
        senLatitude = math.sin(latitudeRadians)
        cosLatitude = math.cos(latitudeRadians)

        # Random angle
        bearing = random.random() * 2 * math.pi
        delta = radius / EARTH_RADIUS
        senBearing = math.sin(bearing)
        cosBearing = math.cos(bearing)
        senDelta = math.sin(delta)
        cosDelta = math.cos(delta)
        resLatRadians = math.asin(senLatitude * cosDelta + cosLatitude * senDelta * cosBearing)
        resLonRadians = longitudeRadians + math.atan2(senBearing * senDelta * cosLatitude,
                                                      cosDelta - senLatitude * math.sin(resLatRadians))
        resLonRadians = ((resLonRadians + (math.pi * 3)) % (math.pi * 2)) - math.pi

        resLatitude = resLatRadians / DEGREES_TO_RADIANS
        resLongitude = resLonRadians / DEGREES_TO_RADIANS

        return GeoPosition(resLatitude, resLongitude)

    @classmethod
    def calculateDistancesByList(self, pointsList):
        """
        :type pointsList: list
        """
        totalDistance = 0.0
        size = len(pointsList)  # type: int
        
        for i in range(size-1, -1, -1):
            currentPoint = GeoPosition(pointsList[i].latitude, pointsList[i].longitude)
            nextPoint = GeoPosition(pointsList[i-1].latitude, pointsList[i-1].longitude)
            totalDistance += currentPoint.distanceTo(nextPoint)

        return totalDistance
