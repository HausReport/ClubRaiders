#   Copyright (c) 2020 Club Raiders Project
#   https://github.com/HausReport/ClubRaiders
#
#   SPDX-License-Identifier: BSD-3-Clause


# sysid, name, rings, res, bodies link
from typing import Dict

#10931: unknown,  # Kokokomi
import craid


class BountyHuntingInfo(object):
    bhDict = {394     : True,  # Abroin
              621     : True,  # Akandi
              798     : True,  # Amalangkan
              1500    : True,  # Aurus
              1542    : False,  # Avik
              2750    : True,  # Caelottixa
              2933    : False,  # Carunda
              3144    : False,  # Certo
              3332    : False,  # Chicoana
              3454    : False,  # Chuelchs
              3576    : True,  # Cofan
              3856    : False,  # Corn Pin
              3975    : True,  # Daik
              4087    : True,  # Delkar
              4170    : True,  # Dhathaarib
              4421    : False,  # Dyavata
              4671    : False,  # Eta Scorpii
              5853    : False,  # Helgaedi
              7734    : True,  # HIP 47156
              8232    : False,  # HIP 67109
              8534    : False,  # HIP 78267
              9130    : False,  # Holler
              9147    : True,  # Honoto
              9261    : True,  # HR 3714
              9556    : False,  # Hun Chonses
              9859    : False,  # Ipilyak
              10511   : False,  # Karitis
              10803   : False,  # Kikapu
              10830   : False,  # Kipsigines
              10977   : True,  # Komovoy
              11559   : False,  # Lapannodaya
              11614   : True,  # LAWD 26
              11884   : False,  # LHS 1951
              11897   : True,  # LHS 2065
              11944   : False,  # LHS 2477
              11974   : True,  # LHS 2887
              12063   : True,  # LHS 380
              12539   : True,  # LPM 607
              12745   : True,  # LTT 4835
              12801   : True,  # LTT 7370
              12908   : False,  # Lu Yupik
              12934   : False,  # Luhman 16
              12977   : False,  # Luyten 674-15
              12978   : True,  # Luyten's Star
              13046   : True,  # Madrus
              13223   : False,  # Mang
              13656   : False,  # Mildeptu
              13664   : True,  # Miller
              13697   : True,  # Minu
              13803   : False,  # Mongan
              13823   : False,  # Mooramba
              14032   : False,  # Nagasairu
              14076   : True,  # Namarii
              14358   : True,  # Ngalia
              14932   : False,  # Oguninksmii
              15003   : False,  # Ondumbo
              15274   : True,  # Panopi
              15443   : True,  # Pemoeri
              15756   : False,  # Procyon
              15976   : False,  # Rana
              16192   : True,  # Ross 446
              16214   : False,  # Ross 591
              16289   : True,  # RR Caeli
              16708   : False,  # Serrot
              16789   : False,  # Shatkwaka
              17073   : True,  # Solati
              17248   : False,  # Surmati
              17325   : True,  # Tabaldak
              17933   : False,  # Trica
              18681   : False,  # Vucub Huan
              19005   : True,  # Wille
              19988   : False,  # Asterope
              19991   : False,  # Atlas
              20053   : True,  # Celaeno
              20550   : False,  # Electra
              20652   : True,  # HIP 17497
              20656   : True,  # HIP 17692
              20712   : True,  # HR 1172
              21120   : True,  # Merope
              21201   : True,  # Pleione
              21389   : True,  # Taygeta
              22431   : True,  # Pleiades Sector DL-Y d65
              22436   : False,  # Pleiades Sector HR-W d1-57
              22438   : False,  # Pleiades Sector HR-W d1-74
              22442   : False,  # Pleiades Sector KC-V c2-11
              23495   : True,  # Robigo
              24005   : False,  # HR 1183
              24460   : False,  # Almagest
              24461   : False,  # Takurua
              24462   : True,  # HIP 8396
              24463   : True,  # Ceos
              27167   : True,  # HIP 17225
              28014   : True,  # HIP 17044
              31053   : True,  # HIP 17892
              32581   : True,  # Pleiades Sector IH-V c2-7
              35347   : True,  # HIP 16753
              35963   : True,  # Pleiades Sector GW-W c1-13
              40994   : True,  # HIP 18077
              44214   : False,  # Pleiades Sector HR-W d1-42
              50090   : True,  # Pleiades Sector PD-S b4-0
              50120   : False,  # Pleiades Sector IH-V c2-16
              53883   : False,  # Col 285 Sector WO-E b13-0
              54280   : False,  # Col 285 Sector BQ-N c7-21
              54282   : False,  # Col 285 Sector YZ-C b14-1
              59230   : True,  # HIP 17412
              68047   : False,  # HIP 72726
              73124   : True,  # Arietis Sector ON-T b3-4
              73732   : True,  # California Sector HR-W d1-28
              81474   : False,  # Synuefe YM-H d11-84
              85934   : False,  # HIP 17655
              125691  : False,  # Pleiades Sector JC-V d2-62
              163300  : True,  # HIP 51352
              207784  : True,  # Pleiades Sector KC-V c2-4
              298089  : True,  # California Sector JH-V c2-12
              339309  : True,  # Col 285 Sector EB-B b15-4
              367160  : True,  # Synuefai EB-R c7-5
              412630  : True,  # Col 285 Sector UE-G c11-19
              494419  : True,  # Wolf 202
              947280  : False,  # 33 Cygni
              2843876 : False,  # Col 285 Sector BQ-N c7-13
              9979032 : False,  # Mel 22 Sector GM-V c2-8
              23118044: True,  # Delphi
              }

    @staticmethod
    def hasRings(sid: int):
        line = BountyHuntingInfo.bhDict.get(sid)
        if line is None:
            return False
        return line



# if __name__ == '__main__':
#     bhDict: Dict[int, bool] = {}
#
#     for item in BountyHuntingInfo.bhArr:
#         sid = item[0]
#         ring: bool = item[2]
#         sname: bool = item[1]
#         print(f"{sid}: {ring},\t\t\t#{sname}")
#
#     # pprint(bhDict)
