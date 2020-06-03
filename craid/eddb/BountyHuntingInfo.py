#   Copyright (c) 2020 Club Raiders Project
#   https://github.com/HausReport/ClubRaiders
#
#   SPDX-License-Identifier: BSD-3-Clause


# sysid, name, rings, res, bodies link
from typing import Dict

bhArr = \
    [[394, 'Abroin', True, 'unknown', 'https://eddb.io/system/bodies/394'],
     [621, 'Akandi', True, 'unknown', 'https://eddb.io/system/bodies/621'],
     [798, 'Amalangkan', True, 'unknown', 'https://eddb.io/system/bodies/798'],
     [1500, 'Aurus', True, 'unknown', 'https://eddb.io/system/bodies/1500'],
     [1542, 'Avik', False, 'unknown', 'https://eddb.io/system/bodies/1542'],
     [2750, 'Caelottixa', True, 'Haz Res', 'https://eddb.io/system/bodies/2750'],
     [2933, 'Carunda', False, 'unknown', 'https://eddb.io/system/bodies/2933'],
     [3144, 'Certo', False, 'unknown', 'https://eddb.io/system/bodies/3144'],
     [3332, 'Chicoana', False, 'unknown', 'https://eddb.io/system/bodies/3332'],
     [3454, 'Chuelchs', False, 'unknown', 'https://eddb.io/system/bodies/3454'],
     [3576, 'Cofan', True, 'unknown', 'https://eddb.io/system/bodies/3576'],
     [3856, 'Corn Pin', False, 'unknown', 'https://eddb.io/system/bodies/3856'],
     [3975, 'Daik', True, 'unknown', 'https://eddb.io/system/bodies/3975'],
     [4087, 'Delkar', True, 'unknown', 'https://eddb.io/system/bodies/4087'],
     [4170, 'Dhathaarib', True, 'unknown', 'https://eddb.io/system/bodies/4170'],
     [4421, 'Dyavata', False, 'unknown', 'https://eddb.io/system/bodies/4421'],
     [4671, 'Eta Scorpii', False, 'unknown', 'https://eddb.io/system/bodies/4671'],
     [5853, 'Helgaedi', False, 'unknown', 'https://eddb.io/system/bodies/5853'],
     [7734, 'HIP 47156', True, 'unknown', 'https://eddb.io/system/bodies/7734'],
     [8232, 'HIP 67109', False, 'unknown', 'https://eddb.io/system/bodies/8232'],
     [8534, 'HIP 78267', False, 'unknown', 'https://eddb.io/system/bodies/8534'],
     [9130, 'Holler', False, 'unknown', 'https://eddb.io/system/bodies/9130'],
     [9147, 'Honoto', True, 'unknown', 'https://eddb.io/system/bodies/9147'],
     [9261, 'HR 3714', True, 'unknown', 'https://eddb.io/system/bodies/9261'],
     [9556, 'Hun Chonses', False, 'unknown', 'https://eddb.io/system/bodies/9556'],
     [9859, 'Ipilyak', False, 'unknown', 'https://eddb.io/system/bodies/9859'],
     [10511, 'Karitis', False, 'unknown', 'https://eddb.io/system/bodies/10511'],
     [10803, 'Kikapu', False, 'unknown', 'https://eddb.io/system/bodies/10803'],
     [10830, 'Kipsigines', False, 'unknown', 'https://eddb.io/system/bodies/10830'],
     [10931, 'Kokokomi', 'unknown', 'unknown', 'https://eddb.io/system/bodies/10931'],
     [10977, 'Komovoy', True, 'unknown', 'https://eddb.io/system/bodies/10977'],
     [11559, 'Lapannodaya', False, 'unknown', 'https://eddb.io/system/bodies/11559'],
     [11614, 'LAWD 26', True, 'unknown', 'https://eddb.io/system/bodies/11614'],
     [11884, 'LHS 1951', False, 'unknown', 'https://eddb.io/system/bodies/11884'],
     [11897, 'LHS 2065', True, 'unknown', 'https://eddb.io/system/bodies/11897'],
     [11944, 'LHS 2477', False, 'unknown', 'https://eddb.io/system/bodies/11944'],
     [11974, 'LHS 2887', True, 'unknown', 'https://eddb.io/system/bodies/11974'],
     [12063, 'LHS 380', True, 'unknown', 'https://eddb.io/system/bodies/12063'],
     [12539, 'LPM 607', True, 'unknown', 'https://eddb.io/system/bodies/12539'],
     [12745, 'LTT 4835', True, 'unknown', 'https://eddb.io/system/bodies/12745'],
     [12801, 'LTT 7370', True, 'unknown', 'https://eddb.io/system/bodies/12801'],
     [12908, 'Lu Yupik', False, 'unknown', 'https://eddb.io/system/bodies/12908'],
     [12934, 'Luhman 16', False, 'unknown', 'https://eddb.io/system/bodies/12934'],
     [12977, 'Luyten 674-15', False, 'unknown', 'https://eddb.io/system/bodies/12977'],
     [12978, "Luyten's Star", True, 'unknown', 'https://eddb.io/system/bodies/12978'],
     [13046, 'Madrus', True, 'unknown', 'https://eddb.io/system/bodies/13046'],
     [13223, 'Mang', False, 'unknown', 'https://eddb.io/system/bodies/13223'],
     [13656, 'Mildeptu', False, 'unknown', 'https://eddb.io/system/bodies/13656'],
     [13664, 'Miller', True, 'unknown', 'https://eddb.io/system/bodies/13664'],
     [13697, 'Minu', True, 'unknown', 'https://eddb.io/system/bodies/13697'],
     [13803, 'Mongan', False, 'unknown', 'https://eddb.io/system/bodies/13803'],
     [13823, 'Mooramba', False, 'unknown', 'https://eddb.io/system/bodies/13823'],
     [14032, 'Nagasairu', False, 'unknown', 'https://eddb.io/system/bodies/14032'],
     [14076, 'Namarii', True, 'unknown', 'https://eddb.io/system/bodies/14076'],
     [14358, 'Ngalia', True, 'unknown', 'https://eddb.io/system/bodies/14358'],
     [14932, 'Oguninksmii', False, 'unknown', 'https://eddb.io/system/bodies/14932'],
     [15003, 'Ondumbo', False, 'unknown', 'https://eddb.io/system/bodies/15003'],
     [15274, 'Panopi', True, 'unknown', 'https://eddb.io/system/bodies/15274'],
     [15443, 'Pemoeri', True, 'unknown', 'https://eddb.io/system/bodies/15443'],
     [15756, 'Procyon', False, 'unknown', 'https://eddb.io/system/bodies/15756'],
     [15976, 'Rana', False, 'unknown', 'https://eddb.io/system/bodies/15976'],
     [16192, 'Ross 446', True, 'unknown', 'https://eddb.io/system/bodies/16192'],
     [16214, 'Ross 591', False, 'unknown', 'https://eddb.io/system/bodies/16214'],
     [16289, 'RR Caeli', True, 'unknown', 'https://eddb.io/system/bodies/16289'],
     [16708, 'Serrot', False, 'unknown', 'https://eddb.io/system/bodies/16708'],
     [16789, 'Shatkwaka', False, 'unknown', 'https://eddb.io/system/bodies/16789'],
     [17073, 'Solati', True, 'unknown', 'https://eddb.io/system/bodies/17073'],
     [17248, 'Surmati', False, 'unknown', 'https://eddb.io/system/bodies/17248'],
     [17325, 'Tabaldak', True, 'unknown', 'https://eddb.io/system/bodies/17325'],
     [17933, 'Trica', False, 'unknown', 'https://eddb.io/system/bodies/17933'],
     [18681, 'Vucub Huan', False, 'unknown', 'https://eddb.io/system/bodies/18681'],
     [19005, 'Wille', True, 'unknown', 'https://eddb.io/system/bodies/19005'],
     [19988, 'Asterope', False, 'unknown', 'https://eddb.io/system/bodies/19988'],
     [19991, 'Atlas', False, 'unknown', 'https://eddb.io/system/bodies/19991'],
     [20053, 'Celaeno', True, 'unknown', 'https://eddb.io/system/bodies/20053'],
     [20550, 'Electra', False, 'unknown', 'https://eddb.io/system/bodies/20550'],
     [20652, 'HIP 17497', True, 'unknown', 'https://eddb.io/system/bodies/20652'],
     [20656, 'HIP 17692', True, 'unknown', 'https://eddb.io/system/bodies/20656'],
     [20712, 'HR 1172', True, 'unknown', 'https://eddb.io/system/bodies/20712'],
     [21120, 'Merope', True, 'unknown', 'https://eddb.io/system/bodies/21120'],
     [21201, 'Pleione', True, 'unknown', 'https://eddb.io/system/bodies/21201'],
     [21389, 'Taygeta', True, 'unknown', 'https://eddb.io/system/bodies/21389'],
     [22431, 'Pleiades Sector DL-Y d65', True, 'unknown', 'https://eddb.io/system/bodies/22431'],
     [22436, 'Pleiades Sector HR-W d1-57', False, 'unknown', 'https://eddb.io/system/bodies/22436'],
     [22438, 'Pleiades Sector HR-W d1-74', False, 'unknown', 'https://eddb.io/system/bodies/22438'],
     [22442, 'Pleiades Sector KC-V c2-11', False, 'unknown', 'https://eddb.io/system/bodies/22442'],
     [23495, 'Robigo', True, 'unknown', 'https://eddb.io/system/bodies/23495'],
     [24005, 'HR 1183', False, 'unknown', 'https://eddb.io/system/bodies/24005'],
     [24460, 'Almagest', False, 'unknown', 'https://eddb.io/system/bodies/24460'],
     [24461, 'Takurua', False, 'unknown', 'https://eddb.io/system/bodies/24461'],
     [24462, 'HIP 8396', True, 'unknown', 'https://eddb.io/system/bodies/24462'],
     [24463, 'Ceos', True, 'unknown', 'https://eddb.io/system/bodies/24463'],
     [27167, 'HIP 17225', True, 'unknown', 'https://eddb.io/system/bodies/27167'],
     [28014, 'HIP 17044', True, 'unknown', 'https://eddb.io/system/bodies/28014'],
     [31053, 'HIP 17892', True, 'unknown', 'https://eddb.io/system/bodies/31053'],
     [32581, 'Pleiades Sector IH-V c2-7', True, 'unknown', 'https://eddb.io/system/bodies/32581'],
     [35347, 'HIP 16753', True, 'unknown', 'https://eddb.io/system/bodies/35347'],
     [35963, 'Pleiades Sector GW-W c1-13', True, 'unknown', 'https://eddb.io/system/bodies/35963'],
     [40994, 'HIP 18077', True, 'unknown', 'https://eddb.io/system/bodies/40994'],
     [44214, 'Pleiades Sector HR-W d1-42', False, 'unknown', 'https://eddb.io/system/bodies/44214'],
     [50090, 'Pleiades Sector PD-S b4-0', True, 'unknown', 'https://eddb.io/system/bodies/50090'],
     [50120, 'Pleiades Sector IH-V c2-16', False, 'unknown', 'https://eddb.io/system/bodies/50120'],
     [53883, 'Col 285 Sector WO-E b13-0', False, 'unknown', 'https://eddb.io/system/bodies/53883'],
     [54280, 'Col 285 Sector BQ-N c7-21', False, 'unknown', 'https://eddb.io/system/bodies/54280'],
     [54282, 'Col 285 Sector YZ-C b14-1', False, 'unknown', 'https://eddb.io/system/bodies/54282'],
     [59230, 'HIP 17412', True, 'unknown', 'https://eddb.io/system/bodies/59230'],
     [68047, 'HIP 72726', False, 'unknown', 'https://eddb.io/system/bodies/68047'],
     [73124, 'Arietis Sector ON-T b3-4', True, 'unknown', 'https://eddb.io/system/bodies/73124'],
     [73732, 'California Sector HR-W d1-28', True, 'unknown', 'https://eddb.io/system/bodies/73732'],
     [81474, 'Synuefe YM-H d11-84', False, 'unknown', 'https://eddb.io/system/bodies/81474'],
     [85934, 'HIP 17655', False, 'unknown', 'https://eddb.io/system/bodies/85934'],
     [125691, 'Pleiades Sector JC-V d2-62', False, 'unknown', 'https://eddb.io/system/bodies/125691'],
     [163300, 'HIP 51352', True, 'unknown', 'https://eddb.io/system/bodies/163300'],
     [207784, 'Pleiades Sector KC-V c2-4', True, 'unknown', 'https://eddb.io/system/bodies/207784'],
     [298089, 'California Sector JH-V c2-12', True, 'unknown', 'https://eddb.io/system/bodies/298089'],
     [339309, 'Col 285 Sector EB-B b15-4', True, 'unknown', 'https://eddb.io/system/bodies/339309'],
     [367160, 'Synuefai EB-R c7-5', True, 'unknown', 'https://eddb.io/system/bodies/367160'],
     [412630, 'Col 285 Sector UE-G c11-19', True, 'unknown', 'https://eddb.io/system/bodies/412630'],
     [494419, 'Wolf 202', True, 'unknown', 'https://eddb.io/system/bodies/494419'],
     [947280, '33 Cygni', False, 'unknown', 'https://eddb.io/system/bodies/947280'],
     [2843876, 'Col 285 Sector BQ-N c7-13', False, 'unknown', 'https://eddb.io/system/bodies/2843876'],
     [9979032, 'Mel 22 Sector GM-V c2-8', False, 'unknown', 'https://eddb.io/system/bodies/9979032'],
     [23118044, 'Delphi', True, 'unknown', 'https://eddb.io/system/bodies/23118044']]

bhDict: Dict[int, bool] = {}
for item in bhArr:
    bhDict[item[0]] = item[2]
