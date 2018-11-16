class Stations:

    def __init__(self, stations):
        # type: (object) -> object
        self.stations = stations

    def comprobar(self):
        invalid_stations = []
        for station in self.stations:
            for station_comnpare in self.stations:
                if station['id'] == station_comnpare['id']:
                    continue
                if station['position']['latitude'] == station_comnpare['position']['latitude'] and station['position']['longitude'] == station_comnpare['position']['longitude']:
                    invalid = station['id'], station_comnpare['id']
                    invalid_stations.append(invalid)
        print (invalid_stations)


