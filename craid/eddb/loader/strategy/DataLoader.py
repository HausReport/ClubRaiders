#   Copyright (c) 2020 Club Raiders Project
#   https://github.com/HausReport/ClubRaiders
#
#   SPDX-License-Identifier: BSD-3-Clause
from abc import ABC, abstractmethod


class DataLoader(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def find_data_file(self, param):
        pass
