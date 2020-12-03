import logging
import os
from typing import Dict

from modules.DailyPlan import DailyPlan
from modules.Status import Status


class LogReporter:

    def __init__(self, logger):
        self.logger = logger

    def report(self, ret: Status, plan: DailyPlan, event: Dict):
        if ret.type != 0:
            self.logger.info( ret.msg)
