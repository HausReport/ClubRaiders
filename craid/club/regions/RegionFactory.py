from craid.club.regions.Region import Region

turnerReach  = Region('Turner Reach',  -270, -200, -350, -175, -175, -250, "circle", "blue")
siriusReach  = Region('Sirius Reach',  -270,  -50, -375, -100, -125,   50, "rect",   "yellow")
corporateWay = Region('Corporate Way',  -95,  150,  110,   75,  -75,  130, "circle", "green")
siriusEast   = Region('Sirius East',    140,  120,  120,   20,  160,  100, "rect",   "yellow")
siriusCore   = Region('Sirius Core',    -20,    0,  -40,  -30,   50,   30, "rect",   "yellow")
pleiades     = Region('Pleiades',       -75, -175, -100, -175,  -50,  -75, "rect",   "orange")
theOldWorlds = Region('The Old Worlds',  70,   80,   60,   10,   80,   60, "rect",   "orange")
gallantBeach = Region('Gallant Beach',  275,  -80,  250, -150,  300, -100, "rect",   "orange")
bentonia     = Region('Bentonia',        30,  120,   25,  135,   40,  175, "rect",   "orange")

regions = [turnerReach, siriusReach, corporateWay, siriusEast, siriusCore, pleiades, theOldWorlds, gallantBeach, bentonia]

rshapes = []
for r in regions:
    foo = dict(type=r.shape,
               xref="x",
               yref="y",
               x0=r.x0,
               y0=r.y0,
               x1=r.x1,
               y1=r.y1,
               opacity=0.2,
               fillcolor=r.color,
               line_color=r.color)
    rshapes.append(foo)

print(rshapes)
