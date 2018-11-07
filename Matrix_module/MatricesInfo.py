from Commons.constants import *
from Matrix_module import DemandMatrix
from Matrix_module import Matrix


class MatricesInfo(object):
    def __init__(self, matrix_week, matrix_weekend):
        self.matrix_week = matrix_week
        self.matrix_weekend = matrix_weekend

    def addCounters(self, counter_days_week, counter_days_weekend, counter_register_r):
        self.counter_days_week = counter_days_week
        self.counter_days_weekend = counter_days_weekend
        self.counter_register_r = counter_register_r
        pass

    def arrayAverage(self):
        array_week = [0] * HOURS
        array_weekend = [0] * HOURS
        for i in range(0, NUM_STATIONS):
            for j in range(0, NUM_STATIONS):
                for h in range(0, HOURS):
                    array_week[h] += self.matrix_week.matrices[i][j][h]
                    array_weekend[h] += self.matrix_weekend.matrices[i][j][h]
        return MatricesInfo(array_week, array_weekend)

    def generateAverageMatrices(self):
        matrix_average_week = DemandMatrix()
        matrix_average_weekend = DemandMatrix()
        total_days_week = self.counter_days_week
        total_days_weekend = self.counter_days_weekend
        for i in range(0, NUM_STATIONS):
            for j in range(0, NUM_STATIONS):
                for h in range(0, HOURS):
                    value_week = float(self.matrix_week.matrices[i][j][h])
                    value_weekend = float(self.matrix_weekend.matrices[i][j][h])
                    if total_days_week > 0:
                        matrix_average_week.matrices[i][j][h] = value_week / total_days_week
                    if total_days_weekend > 0:
                        matrix_average_weekend.matrices[i][j][h] = value_weekend / total_days_weekend

        return MatricesInfo(matrix_average_week, matrix_average_weekend)

    def matrixUsersStationByInstant(self):
        matrix_week = Matrix()
        matrix_weekend = Matrix()
        for i in range(0, NUM_STATIONS):
            for j in range(0, NUM_STATIONS):
                for h in range(0, HOURS):
                    matrix_week.matrices[i][h] += self.matrix_week.matrices[i][j][h]
                    matrix_weekend.matrices[i][h] += self.matrix_weekend.matrices[i][j][h]
        return MatricesInfo(matrix_week, matrix_weekend)

    def generateProbabilityMatrix(self, totalUsersMatrices):
        """

        :param totalUsersMatrices: object with the matrix of total users in week and weekend
        :return: probability matrix in MAtricesinfo Object
        """
        matrix_probability_week = DemandMatrix()
        matrix_probability_weekend = DemandMatrix()
        for i in range(0, NUM_STATIONS):
            for j in range(0, NUM_STATIONS):
                for h in range(0, HOURS):
                    total_users_week = float(totalUsersMatrices.matrix_week.matrices[i][h])
                    total_users_weekend = float(totalUsersMatrices.matrix_weekend.matrices[i][h])
                    aux_users_week = float(self.matrix_week.matrices[i][j][h])
                    aux_users_weekend = float(self.matrix_weekend.matrices[i][j][h])
                    if total_users_week != 0:
                        matrix_probability_week.matrices[i][j][h] = aux_users_week / total_users_week
                    if total_users_weekend != 0:
                        matrix_probability_weekend.matrices[i][j][h] = aux_users_weekend / total_users_weekend

        return MatricesInfo(matrix_probability_week, matrix_probability_weekend)
