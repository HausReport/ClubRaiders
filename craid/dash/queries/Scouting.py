from datetime import datetime, timezone
#from this import Scouting

from dateutil.relativedelta import *

class Scouting:

    def getFilter(self):
        now = datetime.now(timezone.utc)
        lastweek = now + relativedelta(weeks=-1)

        targ = lastweek.strftime("%Y-%m-%d")
        return "{updated} < " + targ

    def getSort(self):
        return [{'column_id': 'distance', 'direction': 'asc'}]

if __name__ == '__main__':
   s = Scouting()
   print(s.getFilter())

