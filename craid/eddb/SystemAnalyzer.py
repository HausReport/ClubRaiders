#   Copyright (c) 2020 Club Raiders Project
#   https://github.com/HausReport/ClubRaiders
#
#   SPDX-License-Identifier: BSD-3-Clause
from InhabitedSystem import InhabitedSystem


class SystemAnalyzer:

    @staticmethod
    def isProbablyAGoodBountyHuntingSystem(sys: InhabitedSystem):
        econ = sys.jsonLine['primary_economy']
        if not econ:
            return False
        if (not econ.startswith('Extract')) and (
                not econ.startswith('Refine')):
            return False
        return True
