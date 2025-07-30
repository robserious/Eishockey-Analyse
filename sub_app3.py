import pandas as pd
import streamlit as st
from datetime import datetime

def team_tabelle_main():
    st.title("📊 Team-Tabelle nach Zeitraum")

    # 1. Datei-Upload
    uploaded_file = st.file_uploader("Wähle eine Spielplan-CSV-Datei", type="csv")

    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file, delimiter=";")

        # 2. Datumskonvertierung
        df["Datum"] = pd.to_datetime(df["Datum"], format="%d.%m.%Y", errors="coerce")
        df = df.dropna(subset=["Datum"])

        # 3. Auswahl des Datumsintervalls
        min_date = df["Datum"].min().date()
        max_date = df["Datum"].max().date()

        start_date, end_date = st.date_input(
            "Zeitraum auswählen", [min_date, max_date], min_value=min_date, max_value=max_date
        )

        if start_date > end_date:
            st.error("❌ Startdatum darf nicht nach dem Enddatum liegen.")
        else:
            zeitraum_df = df[(df["Datum"] >= pd.to_datetime(start_date)) & (df["Datum"] <= pd.to_datetime(end_date))]

            if zeitraum_df.empty:
                st.warning("⚠️ Keine Spiele im gewählten Zeitraum gefunden.")
            else:
                st.success(f"Zeitraum ausgewertet: {start_date} bis {end_date}")

                teams = pd.unique(zeitraum_df[["Home", "Away"]].values.ravel())
                tabelle = []

                for team in teams:
                    spiele = zeitraum_df[(zeitraum_df["Home"] == team) | (zeitraum_df["Away"] == team)]

                    siege = ot_siege = ot_niederlagen = niederlagen = tore_fuer = tore_gegen = 0

                    for _, row in spiele.iterrows():
                        is_home = row["Home"] == team
                        tore_home, tore_away = map(int, row["Resultat"].split(":"))

                        tf = tore_home if is_home else tore_away
                        tg = tore_away if is_home else tore_home
                        tore_fuer += tf
                        tore_gegen += tg

                        if tf > tg:
                            if pd.notna(row["OT/SO"]):
                                ot_siege += 1
                            else:
                                siege += 1
                        elif tf < tg:
                            if pd.notna(row["OT/SO"]):
                                ot_niederlagen += 1
                            else:
                                niederlagen += 1

                    spiele_gesamt = len(spiele)
                    punkte = siege * 3 + ot_siege * 2 + ot_niederlagen * 1
                    punkte_pro_spiel = punkte / spiele_gesamt if spiele_gesamt > 0 else 0
                    torverh = tore_fuer - tore_gegen

                    tabelle.append({
                        "Team": team,
                        "Spiele": spiele_gesamt,
                        "S": siege,
                        "S-OT": ot_siege,
                        "N-OT": ot_niederlagen,
                        "N": niederlagen,
                        "Tore": f"{tore_fuer}:{tore_gegen}",
                        "+/-": torverh,
                        "Punkte": punkte,
                        "Punkte/Spiel": round(punkte_pro_spiel, 2)
                    })

                df_tabelle = pd.DataFrame(tabelle)
                df_tabelle = df_tabelle.sort_values(by=["Punkte", "+/-"], ascending=False).reset_index(drop=True)
                df_tabelle.index += 1

                st.dataframe(df_tabelle)
