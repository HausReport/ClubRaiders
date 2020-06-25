#   Copyright (c) 2020 Club Raiders Project
#   https://github.com/HausReport/ClubRaiders
#
#   SPDX-License-Identifier: BSD-3-Clause
#
#   SPDX-License-Identifier: BSD-3-Clause
import math
from datetime import datetime, timedelta

from craid.eddb.base.Aware import Aware


class System(Aware):

    def __init__(self, jsonLine):
        super().__init__(jsonLine['name'], jsonLine['id'])
        self.x: float = float(jsonLine['x'])
        self.y: float = float(jsonLine['y'])
        self.z: float = float(jsonLine['z'])
        self.needs_permit: bool = jsonLine.get('needs_permit')
        self.updated_at: datetime = datetime.utcfromtimestamp(jsonLine['updated_at'])

    def getX(self) -> float:
        return self.x

    def getY(self) -> float:
        return self.y

    def getZ(self) -> float:
        return self.z

    #
    # Octant of galaxy measured from Etionses
    #
    def getOctant(self) -> int:
        tmp: int = 0
        if self.getX() > 49.5:
            tmp += 1
        if self.getY() > -104:
            tmp += 2
        if self.getZ() > 6.3:
            tmp += 4
        return tmp

    def needsPermit(self) -> bool:
        return self.needs_permit

    def getUpdatedDateTime(self) -> datetime:
        return self.updated_at

    def getUpdatedString(self) -> str:
        days: int = self.getDaysSinceScouted()

        if days <= 1:
            return "Scouted within the last day."

        if days <= 6:
            return "Scouted within the last " + str(days) + " days."

        weeks = math.ceil(days / 7)
        if weeks <= 6:
            return "*Scouted " + str(weeks) + " weeks ago.*"

        return "**Really, really needs to be scouted.**"

    def getDaysSinceScouted(self) -> int:
        upd = self.getUpdatedDateTime()
        now = datetime.utcnow()  # timezone.utc)
        time_elapsed: timedelta = now - upd
        days = time_elapsed.days
        return days

    def getInaraNearestShipyardUrl(self):
        return "https://inara.cz/galaxy-nearest/14/" + str(self.get_id())

    def getInaraSystemUrl(self):
        return "https://inara.cz/galaxy-starsystem/" + str(self.get_id()) + "/"

    def getEddbSystemUrl(self):
        return "https://eddb.io/system/" + str(self.get_id())

    def getRoadToRichesUrl(self):
        return "http://edtools.ddns.net/expl.php?s="  # + urllib.parse.quote(self.get_name())

    def getRegionColor(self):
        from craid.club.regions.RegionFactory import RegionFactory
        return RegionFactory.getRegionColor(self)

    def getRegionName(self):
        from craid.club.regions.RegionFactory import RegionFactory
        return RegionFactory.getRegionName(self)

    def getNearestRegionMessage(self):
        from craid.club.regions.RegionFactory import RegionFactory
        return RegionFactory.getNearestRegionMessage(self)

    def getRegionNumber(self):
        from craid.club.regions.RegionFactory import RegionFactory
        return RegionFactory.getRegionNumber(self)
