def proClubFaction(CurFaction):
    curName = CurFaction.get_name()

    #
    # Weed out negatives first
    #
    if "Alliance Assembly" in curName: return False
    if "Zaonce Jet" in curName: return False

    #
    # Identify positives
    #
    if "Abroin Universal PLC" in curName: return True
    if "Aegis" in curName: return True
    if "Benton" in curName: return True
    # if "Blue Netcoms" in curName: return True
    if "CQC Holding" in curName: return True
    # if "Crimson State" in curName: return True
    if "Emperor's Dawn" in curName: return True
    #if "Emperor's Grace" in curName: return True
    if "Gallant" in curName: return True
    if "Greenventure" in curName: return True
    if "Hodack Prison Colony" in curName: return True
    if "Janus" in curName: return True
    if "Peterson" in curName: return True
    if "Reyan BPS" in curName: return True
    if "Reynhardt IntelliSys" in curName: return True
    if "Rockforth" in curName: return True
    # if "Silver Allied" in curName: return True
    # if "Silver United" in curName: return True
    # if "Silver Universal" in curName: return True
    if "Sirius Atmos" in curName: return True
    if "Sirius Cater" in curName: return True
    if "Sirius Corporation" in curName: return True
    if "Sirius Driv" in curName: return True
    if "Sirius Hot2" in curName: return True
    if "Sirius Hypers" in curName: return True
    if "Sirius Indust" in curName: return True
    if "Sirius Lux" in curName: return True
    if "Sirius Min" in curName: return True
    if "Sirius Pow" in curName: return True
    if "Turner" in curName: return True
    if "Wiggins" in curName: return True
    if "Worldcraft" in curName: return True
    if "Worster" in curName: return True
    if "Wreaken" in curName: return True
    #if "Zaonce" in curName: return True

    return False


def antiClubFactions(CurFaction):
    curName = CurFaction.get_name()
    if "Alliance Assembly" in curName: return True
    if "Mastapolos" in curName: return True
    if "Dark Wheel" in curName: return True
    if "Jet Gang" in curName: return True
    if "Raxxla" in curName: return True
    if "Yupini Limited" in curName: return True
    return False
