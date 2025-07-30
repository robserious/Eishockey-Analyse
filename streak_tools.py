import pandas as pd
from datetime import datetime
import matplotlib.pyplot as plt

def berechne_streaks_von_csv(dateiname, kategorie="P"):
    df = pd.read_csv(dateiname, delimiter=";")

    # Spalten bereinigen und Datum zusammenbauen
    df["Year"] = df["Year"].astype(str)
    df["Datum"] = pd.to_datetime(df["Day"] + "/" + df["Year"], format="%a %d/%m/%Y", errors="coerce")

    df = df.sort_values(by="Datum").reset_index(drop=True)

    streaks = []
    no_streaks = []
    current_streak = 0
    current_no_streak = 0
    max_streak = 0
    max_no_streak = 0

    streak_start = streak_end = None
    no_streak_start = no_streak_end = None
    streak_start_opp = streak_end_opp = None
    no_streak_start_opp = no_streak_end_opp = None

    max_streak_start = max_streak_end = None
    max_no_streak_start = max_no_streak_end = None
    max_streak_start_opp = max_streak_end_opp = None
    max_no_streak_start_opp = max_no_streak_end_opp = None

    for i, row in df.iterrows():
        try:
            wert = int(row[kategorie])
        except:
            wert = 0

        if wert > 0:
            if current_streak == 0:
                streak_start = row["Datum"]
                streak_start_opp = row.get("Opponent", "?")
            current_streak += 1
            streak_end = row["Datum"]
            streak_end_opp = row.get("Opponent", "?")

            if current_no_streak > 0:
                no_streaks.append((current_no_streak, no_streak_start, no_streak_end))
                if current_no_streak > max_no_streak:
                    max_no_streak = current_no_streak
                    max_no_streak_start = no_streak_start
                    max_no_streak_end = no_streak_end
                    max_no_streak_start_opp = no_streak_start_opp
                    max_no_streak_end_opp = no_streak_end_opp
                current_no_streak = 0
        else:
            if current_no_streak == 0:
                no_streak_start = row["Datum"]
                no_streak_start_opp = row.get("Opponent", "?")
            current_no_streak += 1
            no_streak_end = row["Datum"]
            no_streak_end_opp = row.get("Opponent", "?")

            if current_streak > 0:
                streaks.append((current_streak, streak_start, streak_end))
                if current_streak > max_streak:
                    max_streak = current_streak
                    max_streak_start = streak_start
                    max_streak_end = streak_end
                    max_streak_start_opp = streak_start_opp
                    max_streak_end_opp = streak_end_opp
                current_streak = 0

    if current_streak > 0:
        streaks.append((current_streak, streak_start, streak_end))
        if current_streak > max_streak:
            max_streak = current_streak
            max_streak_start = streak_start
            max_streak_end = streak_end
            max_streak_start_opp = streak_start_opp
            max_streak_end_opp = streak_end_opp

    if current_no_streak > 0:
        no_streaks.append((current_no_streak, no_streak_start, no_streak_end))
        if current_no_streak > max_no_streak:
            max_no_streak = current_no_streak
            max_no_streak_start = no_streak_start
            max_no_streak_end = no_streak_end
            max_no_streak_start_opp = no_streak_start_opp
            max_no_streak_end_opp = no_streak_end_opp

    return {
        "max_streak": max_streak,
        "current_streak": current_streak,
        "max_streak_start": max_streak_start,
        "max_streak_end": max_streak_end,
        "max_no_streak": max_no_streak,
        "current_no_streak": current_no_streak,
        "max_no_streak_start": max_no_streak_start,
        "max_no_streak_end": max_no_streak_end,
        "max_streak_start_opp": max_streak_start_opp,
        "max_streak_end_opp": max_streak_end_opp,
        "max_no_streak_start_opp": max_no_streak_start_opp,
        "max_no_streak_end_opp": max_no_streak_end_opp,
        "streaks": streaks,
        "no_streaks": no_streaks
    }

def berechne_alle_streaks_von_csv(dateiname):
    print(f"\n📊 Auswertung für: {dateiname}\n")
    for kategorie, bezeichnung in zip(["P", "G", "A"], ["Punkte", "Tore", "Assists"]):
        result = berechne_streaks_von_csv(dateiname, kategorie)

        vs = lambda d: d.strftime("%Y-%m-%d") if pd.notna(d) else "?"
        so = lambda o: o if o else "?"

        start = vs(result["max_streak_start"])
        end = vs(result["max_streak_end"])
        start_opp = so(result["max_streak_start_opp"])
        end_opp = so(result["max_streak_end_opp"])

        nostart = vs(result["max_no_streak_start"])
        noend = vs(result["max_no_streak_end"])
        nostart_opp = so(result["max_no_streak_start_opp"])
        noend_opp = so(result["max_no_streak_end_opp"])

        print(f"🔁 {bezeichnung}-Streak: {result['max_streak']} (von {start} @{start_opp} bis {end} @{end_opp})")
        print(f"➡️ Aktuell: {result['current_streak']}")

        print(f"🔇 Ohne {bezeichnung}-Streak: {result['max_no_streak']} (von {nostart} @{nostart_opp} bis {noend} @{noend_opp})")
        print(f"➡️ Aktuell ohne: {result['current_no_streak']}\n")

def zeichne_streak_diagramme(dateiname):
    df = pd.read_csv(dateiname, delimiter=";")
    df["Year"] = df["Year"].astype(str)
    df["Datum"] = pd.to_datetime(df["Day"] + "/" + df["Year"], format="%a %d/%m/%Y", errors="coerce")
    df = df.sort_values(by="Datum")

    fig, ax = plt.subplots(figsize=(12, 6))
    for kategorie, farbe in zip(["P", "G", "A"], ["blue", "red", "green"]):
        ax.plot(df["Datum"], df[kategorie], marker="o", linestyle="-", label=kategorie, color=farbe)

    ax.set_title("Verlauf: Punkte, Tore, Assists")
    ax.set_xlabel("Datum")
    ax.set_ylabel("Wert pro Spiel")
    ax.legend()
    plt.grid(True)
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

def berechne_alle_streaks_von_df(df):
    if "Player" not in df.columns:
        return None
    spielername = df["Player"].iloc[0]
    return berechne_streaks(df, spielername)
