#   Copyright (c) 2020 Club Raiders Project
#   https://github.com/HausReport/ClubRaiders
#
#   SPDX-License-Identifier: BSD-3-Clause
import math


class Strategy:
    def expandOneDay(self, inf: float, pop: int):
        top = (36 - math.log(pop, 2))
        bottom = (100 + (36 - math.log(pop, 2)))
        ret = 100.0 * (inf + top) / bottom
        if ret > 100.0:
            ret = 100.0
        if ret < 1.0:
            ret = 1.0
        return ret

    def dailyIncrease(self, inf: float, pop: int):
        return self.expandOneDay(inf, pop) - inf

    def retreatOneDay(self, inf: float, pop: int):
        top = (36 - math.log(pop, 2))
        bottom = (100 + (36 - math.log(pop, 2)))
        ret = inf - ((100 * ((100 - inf) + top) / bottom) - (100 - inf))
        if ret > 100.0:
            ret = 100.0
        if ret < 1.0:
            ret = 1.0
        return ret

    def dailyDecrease(self, inf: float, pop: int):
        return self.expandOneDay(inf, pop) - inf
