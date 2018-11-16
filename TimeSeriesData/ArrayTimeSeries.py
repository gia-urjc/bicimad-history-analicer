from TimeSeriesData.timeSeriesData import TimeSeriesData


class ArrayTimeSeries(object):
    def __init__(self):
        self.array = list()

    def addValue(self, __id, __date):
        for i in self.array:  # type: TimeSeriesData
            if i.id_station == __id and i.date == __date:
                i.amount += 1
                break
