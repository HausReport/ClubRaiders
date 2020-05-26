from datetime import datetime, timezone

from dateutil.relativedelta import *


# from this import Scouting

class Scouting:

    @staticmethod
    def getFilter(self):
        now = datetime.now(timezone.utc)
        lastweek = now + relativedelta(weeks=-1)

        targ = lastweek.strftime("%Y-%m-%d")
        return "{updated} < " + targ

    @staticmethod
    def getSort(self):
        return [{'column_id': 'distance', 'direction': 'asc'}]


if __name__ == '__main__':
    s = Scouting()
    print(s.getFilter())
