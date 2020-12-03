from typing import List, Dict

from modules.DailyPlan import DailyPlan
from modules.LogReporter import LogReporter


class DailyPlans:

    def __init__(self, reporter: LogReporter):
        self.plans: List[DailyPlan] = []
        self.reporter = reporter

    def addPlan(self, plan: DailyPlan):
        self.plans.add(plan)

    #
    # Updated by DailyPlans as ship moves
    #
    def setCurrentSystem(self, sys: str):
        for plan in self.plans:
            plan.setCurrentSystem(sys)

    def setCurrentSystemFactions(self, factions: List[str]):
        for plan in self.plans:
            plan.setCurrentSystemFactions(factions)

    def setCurrentStation(self, sta: str):
        for plan in self.plans:
            plan.setCurrentSystemStation(sta)

    def setCurrentStationFaction(self, fac:str):
        for plan in self.plans:
            plan.setCurrentSystemStationFaction(fac)


    #
    # Checks against each of the plans in the list
    #
    def checkMissionSuccess(self, event: Dict):
        for plan in self.plans:
            ret = plan.checkMissionSuccess(event)
            self.report(ret, plan, event)

    def checkBounty(self, event: Dict):
        for plan in self.plans:
            ret = plan.checkBounty(event)
            self.report(ret, plan, event)

    def checkCartography(self, event: Dict):
        for plan in self.plans:
            ret = plan.checkCartography(event)
            self.report(ret, plan, event)

    def checkTrade(self, event: Dict):
        for plan in self.plans:
            ret = plan.checkTrade(event)
            self.report(ret, plan, event)

    def checkMissionFail(self, event: Dict):
        for plan in self.plans:
            ret = plan.checkMissionFail(event)
            self.report(ret, plan, event)

    def checkMurder(self, event: Dict):
        for plan in self.plans:
            ret = plan.checkMurder(event)
            self.report(ret, plan, event)

    def report(self, ret: int, plan: DailyPlan, event: Dict):
        self.reporter.report(ret, plan, event)

