# System Name
# Hero Faction
# Target Faction
# Webhook?


# === Positive Levers ===
# Mission Completion (ez)              -- ALWAYS
# Bounties (ez)                        -- OPTIONAL
# Cartographic Data (ez)               -- OPTIONAL
# Trade at Profit (ez)                 -- OPTIONAL

# === Negative Levers ===
# Mission Fails (needs backing table)  -- ALWAYS
# Trade at Loss (ez)                   -- OPTIONAL
# Clean Murders (needs backing table)  -- ALWAYS

# === Special Circumstances
# War - Bonds
# War - CZ Wins
# War - Bounties
# Election?
# Draught?
# Infrastructure Failure?
# Other states?
from typing import List, Dict

from modules import GlobalDictionaries
from modules.Status import Status


class DailyPlan:
    #
    # Plan statics
    #
    systemName = None
    # systemAddress = None
    heroFaction = None
    targetFaction = None

    #
    # Movement based
    #
    currentSystem = None
    # currentSystemAddress = None
    currentSystemFactions = None
    currentStation = None

    #
    # Goals
    #
    missionInfluenceGoal = 0
    bountyGoal = 0
    cartographyGoal = 0
    tradeProfitGoal = 0
    missionFailGoal = 0
    tradeLossGoal = 0
    murderGoal = 0

    def __init__(self, systemName, heroFaction, targetFaction):
        self.systemName = systemName
        self.heroFaction = heroFaction
        self.targetFaction = targetFaction

    def isSystemName(self, name: str) -> bool:
        return name.lower() == self.systemName.lower()

    def isHeroFactionName(self, name: str) -> bool:
        return name.lower() == self.heroFaction.lower()

    def isTargetFactionName(self, name: str) -> bool:
        return name.lower() == self.targetFaction.lower()

    def isNeitherFactionName(self, name: str) -> bool:
        if not self.isHeroFactionName(name):
            if not self.isTargetFactionName():
                return True
        return False

    #
    # Updated by DailyPlans as ship moves
    #
    def setCurrentSystem(self, sys: str):
        self.currentSystem: str = sys
        # self.currentSystemAddress: str = add
        #
        # FIXME: Not sure if this makes sense
        # Say that you log in in a different system and submit a mission,
        # the systemAddress may not have been set.
        # Maybe initialize systemaddresses when getting the missions event?
        #
        # if self.isSystemName(sys):
        # if self.systemAddress is None:
        # self.systemAddress = add

    def setCurrentSystemFactions(self, facs: List[str]):
        self.currentSystemFactions: List[str] = facs

    def setCurrentStation(self, sta: str):
        self.currentStation: str = sta

    #
    # Positive Levers
    #
    def addMissionInfluenceGoal(self, miss: int = 60):
        self.missionInfluenceGoal = miss

    def addBountyGoal(self, bounty: int = 4000000):
        self.bountyGoal = bounty

    def addCartographyGoal(self, cart: int = 12000000):
        self.cartographyGoal = cart

    def addTradeProfitGoal(self, prof: int = 16000000):
        self.tradeProfitGoal = prof

    #
    # Negative Levers
    #
    def addMissionFailGoal(self, miss: int = 12):
        self.missionFailGoal = miss

    def addTradeLossGoal(self, loss: int = 16000000):
        self.tradeLossGoal = loss

    def addMurderGoal(self, murd: int = 12):
        self.murderGoal = murd

    #
    # Lever checks
    # return -1 for harmful action
    # return 0 for neutral action
    # return +1 for helpful action
    #
    def checkMissionSuccess(self, entry: Dict) -> List[Status]:
        ret: List[Status] = []
        factionEffects = entry['FactionEffects']

        for effect in factionEffects:
            factionName = effect['Faction']
            influenceEntries = effect['Influence']
            print(factionName)
            for influenceEntry in influenceEntries:
                entrySystemAddress = str(influenceEntry['SystemAddress'])
                entrySystemName = GlobalDictionaries.getSystemByAddress(entrySystemAddress)
                inf = len(influenceEntry['Influence'])
                if self.isSystemName(entrySystemName):  # FIXME: revisit case of two systems with same name
                    if self.isHeroFactionName(factionName):
                        msg = f"Mission Contribution for Hero Faction {factionName} of {inf} points."
                        ret.add(Status(1, msg))
                    elif self.isTargetFactionName(factionName):
                        msg = f"Mission Contribution for Target Faction {factionName} of {inf} points."
                        ret.add(Status(-1, msg))
                    else:
                        msg = f"Mission Contribution for Competitor Faction {factionName} of {inf} points."
                        ret.add(Status(-1, msg))

        return ret

    def checkBounty(self, event: Dict) -> List[Status]:
        a = 4
        #
        # If benefits hero faction in goal system
        #
        if a == 0:
            return Status(1, "Bounty Contribution for Hero Faction")

        #
        # If benefits target faction in goal system
        #
        if a == 0:
            return Status(-1, "Bounty Contribution for Enemy Faction")

        #
        # If benefits competitor faction in goal system
        #
        if a == 0:
            return Status(-1, "Bounty Contribution for Competitor Faction")

        #
        # Otherwise
        #
        return Status(0, "No effect bounty")

    def checkCartography(self, event: Dict) -> List[Status]:
        if this.StationFaction.get().lower() == this.FactionName.get().lower() and this.SystemName.get().lower() == system.lower():
            this.CartDataSold.set(this.CartDataSold.get() + entry['TotalEarnings'])
            this.cartdata2["text"] = human_format(this.CartDataSold.get())
        a = 4
        #
        # If benefits hero faction in goal system
        #
        if a == 0:
            return Status(1, "Cartography Contribution for Hero Faction")

        #
        # If benefits target faction in goal system
        #
        if a == 0:
            return Status(1, "Cartography Contribution for Enemy Faction")

        #
        # If benefits competitor faction in goal system
        #
        if a == 0:
            return Status(1, "Cartography Contribution for Competitor Faction")

        #
        # Otherwise
        #
        return Status(1, "No Effect Cartography Contribution")

    def checkTrade(self, event: Dict) -> List[Status]:
        # handle profit and loss cases
        a = 4
        #
        # If benefits hero faction in goal system
        #
        if a == 0:
            return Status(1, "Trade Contribution for Hero Faction")

        #
        # If benefits target faction in goal system
        #
        if a == 0:
            return Status(-1, "Trade Contribution for Enemy Faction")

        #
        # If benefits competitor faction in goal system
        #
        if a == 0:
            return Status(-1, "Trade Contribution for Competitor Faction")

        #
        # Otherwise
        #
        return Status(0, "No Effect Trade Contribution")

    def checkMissionFail(self, event: Dict) -> List[Status]:
        a = 4
        #
        # If attacks enemy faction in goal system
        #
        if a == 0:
            return Status(1, "Failed Mission against Enemy Faction")

        #
        # If benefits hero faction in goal system
        #
        if a == 0:
            return Status(-1, "Failed Mission against Hero Faction")

        #
        # If benefits competitor faction in goal system
        #
        if a == 0:
            return Status(-1, "Failed Mission against Neutral Faction")

        #
        # Otherwise
        #
        return Status(0, "No Effect Failed Mission")

    def checkMurder(self, event: Dict) -> List[Status]:
        a = 4
        #
        # If attacks enemy faction in goal system
        #
        if a == 0:
            return Status(1, "Murder against Enemy Faction")

        #
        # If attacks hero faction in goal system
        #
        if a == 0:
            return Status(-1, "Murder against Hero Faction")

        #
        # If attacks neutral faction in goal system
        #
        if a == 0:
            return Status(-1, "Murder against Neutral Faction")

        #
        # Otherwise
        #
        return Status(0, "No effect Murder")
