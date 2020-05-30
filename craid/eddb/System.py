#   Copyright (c) 2020 Club Raiders Project
#   https://github.com/HausReport/ClubRaiders
#
#   SPDX-License-Identifier: BSD-3-Clause
import math
from datetime import datetime, timedelta

from Aware import Aware


class System(Aware):

    def __init__(self, jsonString: str):
        super().__init__(jsonString)

    def getX(self) -> float:
        return float(self.jsonLine['x'])

    def getY(self) -> float:
        return float(self.jsonLine['y'])

    def getZ(self) -> float:
        return float(self.jsonLine['z'])

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
        prm: bool = self.jsonLine.get('needs_permit')
        return prm

    def getUpdatedDateTime(self) -> datetime:
        return datetime.utcfromtimestamp(self.jsonLine['updated_at'])

    def getUpdatedString(self) -> str:
        upd = self.getUpdatedDateTime()
        now = datetime.utcnow()  # timezone.utc)
        time_elapsed: timedelta = now - upd
        days = time_elapsed.days

        if days <= 1:
            return "Scouted within the last day."

        if days <= 6:
            return "Scouted within the last " + str(days) + " days."

        weeks = math.ceil(days / 7)
        if weeks <= 6:
            return "*Scouted " + str(weeks) + " weeks ago.*"

        return "**Really, really needs to be scouted.**"

    def getInaraNearestShipyardUrl(self):
        return "https://inara.cz/galaxy-nearest/14/" + str(self.get_id())

    def getInaraSystemUrl(self):
        return "https://inara.cz/galaxy-starsystem/" + str(self.get_id()) + "/"

    def getEddbSystemUrl(self):
        return "https://eddb.io/system/" + str(self.get_id())

    def getRoadToRichesUrl(self):
        return "http://edtools.ddns.net/expl.php?s=" #+ urllib.parse.quote(self.get_name())
