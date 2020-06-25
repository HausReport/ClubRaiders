import craid
from craid.club.regions.MultiSphericalRegion import MultiSphericalRegion
from craid.club.regions.SphericalRegion import SphericalRegion
from craid.club.regions.TheUnregion import TheUnregion


# from craid.eddb.System import System
# 4: SphericalRegion("Sirius", 4, 6, -6, -1, 35, 'rgb(255, 255, 0)'),
# 5: SphericalRegion("Ega-Cd", 5, 25, 96, 4, 50, 'rgb(0,255,0)'),
# 7: SphericalRegion("Hodack", 8, 60, 46, 23, 45, 'rgb(0,255,255)'),

# TODO: might be a better pallete https://learnui.design/tools/data-color-picker.html#divergent
from craid.eddb.faction.SquadronXYZ import SquadronXYZ


class RegionFactory(object):
    unRegion = TheUnregion()
    regionDict = {
        "No Region" : unRegion,
        "Merope"    : SphericalRegion("Merope",        1,  -79,  -150, -340, 100, 'rgb(255, 0, 0)'),
        "Rectangle" : SphericalRegion("Rectangle",     2,  -54,   -66, -124,  75, 'rgb(255,255,0)'),
        "California": SphericalRegion("California",    3, -320,  -217, -913, 200, 'rgb(32,32,32)'),
        "Sirius"    : SphericalRegion("Sirius",        4,    6,    -1,   -6,  35, 'rgb(0, 255, 0)'),
        "Xi Shan"   : SphericalRegion("Xi Shan",       5,  155,    84,  -50,  45, 'rgb(255,0,255)'),
        "Abroin"    : SphericalRegion("Abroin",        6,  -94,   110,  -40,  30, 'rgb(0,255,255)'),
        "Bentonia"  : SphericalRegion("Bentonia",      7,   27,   151,  -81,  35, 'rgb(0,0,255)'),
        "Hodack"    : SphericalRegion("Hodack",        8,   60,    23,   46,  35, 'rgb(0,0,255)'),
        "Wreaken"   : SphericalRegion("Wreaken",       9,   32,    18,  114,  25, 'rgb(0,0,255)'),
        "CQC"       : SphericalRegion("CQC",          10,   18,   -11,   78,  30, 'rgb(0,0,255)'),
    }

    @staticmethod
    def getRegion(x, y, z) -> SphericalRegion:
        for key in RegionFactory.regionDict.keys():
            reg = RegionFactory.regionDict.get(key)
            if reg.contains(x, y, z):
                return reg

        return RegionFactory.unRegion

    @staticmethod
    def getRegionByName(x:int) -> SphericalRegion:
        reg = RegionFactory.regionDict.get(x)
        if reg is None:
            return RegionFactory.unRegion

        return reg

    # @staticmethod
    # def getRegion(sys: craid.eddb.System.System) -> SphericalRegion:
    #     return RegionFactory.getRegion(sys.getX(), sys.getY(), sys.getZ())

    # @staticmethod
    # def getRegionNumber(x, y, z) -> int:
    #     reg: SphericalRegion = RegionFactory.getRegion(x,y,z)
    #     if reg is None:
    #         return 0
    #
    #     return reg.getNumber()

    @staticmethod
    def getRegionNumber(sys: craid.eddb.system.System.System) -> SphericalRegion:
        reg: SphericalRegion = RegionFactory.getRegion(sys.getX(), sys.getY(), sys.getZ())
        if reg is None:
            return 0

        return reg.getNumber()

    @staticmethod
    def getRegionColor(x, y, z) -> int:
        reg: SphericalRegion = RegionFactory.getRegion(x, y, z)
        if reg is None:
            return RegionFactory.unRegion.getColor()

        return reg.getColor()

    @staticmethod
    def getRegionColor(sys: craid.eddb.system.System.System) -> SphericalRegion:
        reg = RegionFactory.getRegion(sys.getX(), sys.getY(), sys.getZ())
        return reg.getColor()

    @staticmethod
    def getRegionName(sys: craid.eddb.system.System.System) -> SphericalRegion:
        reg = RegionFactory.getRegion(sys.getX(), sys.getY(), sys.getZ())
        return reg.getTitle()

    @staticmethod
    def getNearestRegionMessage(sys: craid.eddb.system.System.System) -> str:
        closestDist = 999999.0
        closestRegion: SphericalRegion = None

        for key in RegionFactory.regionDict.keys():
            item = RegionFactory.regionDict.get(key)
            d2 = item.distanceFrom(sys.getX(), sys.getY(), sys.getZ())
            if d2 < closestDist:
                closestRegion = item
                closestDist = d2
                if closestDist == 0.0:
                    break

        if closestDist == 0.0:
            return f'in {closestRegion.getTitle()}'
        else:
            closestDistStr = "{:,.0f}".format(closestDist)
            return f'{closestDistStr} ly from {closestRegion.getTitle()}'

    @staticmethod
    def getSquadronRegion(squadName: str, radius: float, color: str):
        aDict = SquadronXYZ.myDict.get(squadName)
        if aDict is None:
            return RegionFactory.unRegion

        rData = []
        for aName in aDict.keys():
            point = aDict.get(aName)
            px = point[0]
            py = point[1]
            pz = point[2]
            rData.append( (aName, px, py, pz))

        return MultiSphericalRegion(squadName, -1, rData, radius, color)
