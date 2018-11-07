import dateutil.parser

from Commons.constants import *


class DemandMatrix(object):

    def __init__(self):
        self.matrices = []
        for i in range(0, NUM_STATIONS + 1):
            self.matrices.append([])
            for j in range(0, NUM_STATIONS + 1):
                self.matrices[i].append([])
                for h in range(0, HOURS):
                    self.matrices[i][j].append([])
                    self.matrices[i][j][h] = 0

    def __index__(self, demandMatrix):
        self.matrices = demandMatrix

    def addValue(self, json_line, numStation):
        date = dateutil.parser.parse(json_line["unplug_hourTime"]["date"])
        hour = date.hour
        id_init_station = json_line["idunplug_station"]
        id_end_station = json_line["idplug_station"]
        if id_init_station < numStation and id_end_station < numStation:
            self.matrices[id_init_station][id_end_station][hour] += 1
