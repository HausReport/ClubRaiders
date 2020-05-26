from datetime import datetime, timezone

from dateutil.relativedelta import *


# from this import Scouting

class Scouting:

    @staticmethod
    def getFilter():
        now = datetime.now(timezone.utc)
        lastWeek = now + relativedelta(weeks=-1)

        targetDate = lastWeek.strftime("%Y-%m-%d")
        return "{updated} < " + targetDate

    @staticmethod
    def getSort():
        return [{'column_id': 'distance', 'direction': 'asc'}]


if __name__ == '__main__':
    s = Scouting()
    print(Scouting.getFilter())
