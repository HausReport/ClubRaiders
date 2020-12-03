"""
Example EDMC plugin.
It adds a single button to the EDMC interface that displays the number of times it has been clicked.
"""

#   Copyright (c) 2020 Club Raiders Project
#   https://github.com/HausReport/ClubRaiders
#
#   SPDX-License-Identifier: BSD-3-Clause

import logging
import os
import tkinter as tk
from typing import Optional, Set, List

import myNotebook as nb
from config import appname, config

import modules.ClubFactionNames

#PLUGIN_NAME = "edmClub"
# This could also be returned from plugin_start3()
from modules.DailyPlans import DailyPlans
from modules.LogReporter import LogReporter

plugin_name = os.path.basename(os.path.dirname(__file__))

# A Logger is used per 'found' plugin to make it easy to include the plugin's
# folder name in the logging output format.
# NB: plugin_name here *must* be the plugin's folder name as per the preceding
#     code, else the logger won't be properly set up.
logger = logging.getLogger(f'{appname}.{plugin_name}')

# If the Logger has handlers then it was already set up by the core code, else
# it needs setting up here.
if not logger.hasHandlers():
    level = logging.INFO  # So logger.info(...) is equivalent to print()

    logger.setLevel(level)
    logger_channel = logging.StreamHandler()
    logger_formatter = logging.Formatter(f'%(asctime)s - %(name)s - %(levelname)s - %(module)s:%(lineno)d:%(funcName)s: %(message)s')
    logger_formatter.default_time_format = '%Y-%m-%d %H:%M:%S'
    logger_formatter.default_msec_format = '%s.%03d'
    logger_channel.setFormatter(logger_formatter)
    logger.addHandler(logger_channel)

logReporter: LogReporter = LogReporter(logger)
FACTION_HERO = 1
FACTION_NONE = 0
FACTION_COMPETITOR = -1
FACTION_TARGET = -2

class edmClub:
    """
    ClickCounter implements the EDMC plugin interface.
    It adds a button to the EDMC UI that displays the number of times it has been clicked, and a preference to set
    the number directly.
    """

    def __init__(self) -> None:
        # Be sure to use names that wont collide in our config variables
        self.click_count: Optional[tk.StringVar] = tk.StringVar(value=str(config.getint('click_counter_count')))
        logger.info("ClickCounter instantiated")

    def on_load(self) -> str:
        """
        on_load is called by plugin_start3 below.
        It is the first point EDMC interacts with our code after loading our module.
        :return: The name of the plugin, which will be used by EDMC for logging and for the settings window
        """
        return plugin_name

    def on_unload(self) -> None:
        """
        on_unload is called by plugin_stop below.
        It is the last thing called before EDMC shuts down. Note that blocking code here will hold the shutdown process.
        """
        self.on_preferences_closed("", False)  # Save our prefs

    def setup_preferences(self, parent: nb.Notebook, cmdr: str, is_beta: bool) -> Optional[tk.Frame]:
        """
        setup_preferences is called by plugin_prefs below.
        It is where we can setup our own settings page in EDMC's settings window. Our tab is defined for us.
        :param parent: the tkinter parent that our returned Frame will want to inherit from
        :param cmdr: The current ED Commander
        :param is_beta: Whether or not EDMC is currently marked as in beta mode
        :return: The frame to add to the settings window
        """
        current_row = 0
        frame = nb.Frame(parent)

        # setup our config in a "Click Count: number"
        nb.Label(frame, text='Click Count').grid(row=current_row)
        nb.Entry(frame, textvariable=self.click_count).grid(row=current_row, column=1)
        current_row += 1  # Always increment our row counter, makes for far easier tkinter design.
        return frame

    def on_preferences_closed(self, cmdr: str, is_beta: bool) -> None:
        """
        on_preferences_closed is called by prefs_changed below.
        It is called when the preferences dialog is dismissed by the user.
        :param cmdr: The current ED Commander
        :param is_beta: Whether or not EDMC is currently marked as in beta mode
        """
        config.set('click_counter_count', self.click_count.get())

    def setup_main_ui(self, parent: tk.Frame) -> tk.Frame:
        """
        Create our entry on the main EDMC UI.
        This is called by plugin_app below.
        :param parent: EDMC main window Tk
        :return: Our frame
        """
        current_row = 0
        frame = tk.Frame(parent)
        button = tk.Button(
            frame,
            text="Count me",
            command=lambda: self.click_count.set(str(int(self.click_count.get()) + 1))
        )
        button.grid(row=current_row)
        current_row += 1
        nb.Label(frame, text="Count:").grid(row=current_row, sticky=tk.W)
        nb.Label(frame, textvariable=self.click_count).grid(row=current_row, column=1)
        return frame


cc = edmClub()


# Note that all of these could be simply replaced with something like:
# plugin_start3 = cc.on_load
def plugin_start3(plugin_dir: str) -> str:
    return cc.on_load()


def plugin_stop() -> None:
    return cc.on_unload()


def plugin_prefs(parent: nb.Notebook, cmdr: str, is_beta: bool) -> Optional[tk.Frame]:
    return cc.setup_preferences(parent, cmdr, is_beta)


def prefs_changed(cmdr: str, is_beta: bool) -> None:
    return cc.on_preferences_closed(cmdr, is_beta)


def plugin_app(parent: tk.Frame) -> Optional[tk.Frame]:
    return cc.setup_main_ui(parent)


# def is_system_of_interest() -> bool:
#     return False
#
# def is_target_faction() -> bool:
#     return False
#
# def is_hero_faction() -> bool:
#     return False
#
# def is_competitor_faction() -> bool:
#     return False

dailyPlans: DailyPlans = DailyPlans(logReporter)

def journal_entry(cmdr, is_beta, system, station, entry, state):
    event = entry['event']

    if event == 'Docked' or (event =='Location' and entry['Docked']==True):
        sf = entry['StationFaction']
        sa = entry['SystemAddress']
        ss = entry['StarSystem']
        stationFactionName = sf['Name']
        dailyPlans.setCurrentSystem(ss)
        dailyPlans.setCurrentStation(station)
        dailyPlans.setCurrentStationFaction(stationFactionName)
        modules.globals.add_system_and_address(ss, sa)
    elif event == 'Undocked':
        dailyPlans.setCurrentStation(None)
        dailyPlans.setCurrentStationFaction(None)
    elif (event == 'Location'):
        sn = entry['StarSystem']
        sa = entry['SystemAddress']
        dailyPlans.setCurrentSystem(sn)
        dailyPlans.setCurrentStation(None)
        dailyPlans.setCurrentStationFaction(None)
        modules.globals.add_system_and_address(sn, sa)
    elif event == 'MissionCompleted':  # get mission influence value
        dailyPlans.checkMissionSuccess(event)
    elif ( (event == 'SellExplorationData') or (event == 'MultiSellExplorationData')) :  # get carto data value
        dailyPlans.checkCartography(event)
    elif (event == 'RedeemVoucher' and entry['Type'] == 'bounty'):  # bounties collected
        dailyPlans.checkBounty(event)
    elif event == 'MarketSell':  # Trade Profit
        if this.StationFaction.get().lower() == this.FactionName.get().lower() and this.SystemName.get().lower() == system.lower():
            cost = entry['Count'] * entry['AvgPricePaid']
            profit = entry['TotalSale'] - cost
            this.TradeProfit.set(this.TradeProfit.get() + profit)
            this.tradeprofit2['text'] = human_format(this.TradeProfit.get())

    elif event == 'FSDJump' or event == 'CarrierJump':  # get factions at jump
        #
        # Update system stuff
        #
        sn = entry['StarSystem']
        sa = entry['SystemAddress']
        dailyPlans.setCurrentSystem(sn)
        dailyPlans.setCurrentStation(None)
        dailyPlans.setCurrentStationFaction(None)
        modules.globals.add_system_and_address(sn, sa)

        #
        # Update faction stuff
        #
        this.FactionNames = []
        this.FactionStates = {'Factions': []}
        z = 0
        for i in entry['Factions']:
            if i['Name'] == "Pilots' Federation Local Branch":
                continue

            this.FactionNames.append(i['Name'])
            this.FactionStates['Factions'].append(
                {'Faction': i['Name'], 'Happiness': i['Happiness_Localised'], 'States': []})

            try:
                for x in i['ActiveStates']:
                    this.FactionStates['Factions'][z]['States'].append({'State': x['State']})
            except KeyError:
                this.FactionStates['Factions'][z]['States'].append({'State': 'None'})
            z += 1

    # FIXME: set system, factions, address, etc at CarrierJump also