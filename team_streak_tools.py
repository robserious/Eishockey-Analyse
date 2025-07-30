import pandas as pd

def berechne_team_streaks(df, teamname):
    df["Datum"] = pd.to_datetime(df["Datum"], format="%d.%m.%Y", errors="coerce")
    df = df.sort_values(by="Datum")

    spiele = df[(df["Home"] == teamname) | (df["Away"] == teamname)].copy()
    spiele["ist_heimspiel"] = spiele["Home"] == teamname

    def berechne_punkte(row):
        ist_heim = row["ist_heimspiel"]
        tore_team = int(row["Resultat"].split(":")[0 if ist_heim else 1])
        tore_gegner = int(row["Resultat"].split(":")[1 if ist_heim else 0])

        if tore_team > tore_gegner:
            return 3
        elif tore_team == tore_gegner:
            if row["OT/SO"] in ["OT", "SO"]:
                return 2
            else:
                return 1  # theoretischer Gleichstand ohne OT/SO (unwahrscheinlich)
        else:
            if row["OT/SO"] in ["OT", "SO"]:
                return 1
            else:
                return 0

    spiele["Punkte"] = spiele.apply(berechne_punkte, axis=1)

    max_winstreak = 0
    max_nowin_streak = 0
    current_winstreak = 0
    current_nowin_streak = 0

    max_winstreak_start = max_winstreak_end = None
    max_nowin_streak_start = max_nowin_streak_end = None
    current_start_win = current_start_nowin = None

    for i, row in spiele.iterrows():
        punkte = row["Punkte"]
        datum = row["Datum"]

        if punkte >= 2:
            if current_winstreak == 0:
                current_start_win = datum
            current_winstreak += 1
            if current_winstreak > max_winstreak:
                max_winstreak = current_winstreak
                max_winstreak_start = current_start_win
                max_winstreak_end = datum
            current_nowin_streak = 0
        else:
            if current_nowin_streak == 0:
                current_start_nowin = datum
            current_nowin_streak += 1
            if current_nowin_streak > max_nowin_streak:
                max_nowin_streak = current_nowin_streak
                max_nowin_streak_start = current_start_nowin
                max_nowin_streak_end = datum
            current_winstreak = 0

    result = {
        "max_winstreak": max_winstreak,
        "max_winstreak_start": max_winstreak_start,
        "max_winstreak_end": max_winstreak_end,
        "current_winstreak": current_winstreak,
        "max_nowin_streak": max_nowin_streak,
        "max_nowin_streak_start": max_nowin_streak_start,
        "max_nowin_streak_end": max_nowin_streak_end,
        "current_nowin_streak": current_nowin_streak,
    }

    return result
