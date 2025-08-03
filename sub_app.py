import pandas as pd
import streamlit as st
from streak_tools import berechne_streaks_von_csv
from utils import read_csv_with_delimiter_detection

def spieler_main():
    st.title("🧊 Spieleranalyse – Streaks")

    uploaded_file = st.file_uploader("Wähle eine CSV-Datei", type="csv")

    if uploaded_file is not None:
        df = read_csv_with_delimiter_detection(uploaded_file)
        df.columns = df.columns.str.strip()

        spalten = df.columns

        is_spielerliste = "Spieler" in spalten and "PTS" in spalten
        is_gamelog = "Player" in spalten and "Year" in spalten and "Day" in spalten

        if is_spielerliste:
            st.subheader("📋 Spielerliste erkannt")

            option = st.selectbox(
                "Was möchtest du anzeigen?",
                ["Top-Spieler (nach Punkten)", "Top-Torschützen", "Top-Vorbereiter"]
            )

            if option == "Top-Spieler (nach Punkten)":
                df["PTS"] = pd.to_numeric(df["PTS"], errors="coerce").fillna(0)
                top = df.sort_values(by="PTS", ascending=False).head(10)
                st.dataframe(top[["Spieler", "Team", "PTS"]])

            elif option == "Top-Torschützen":
                df["G"] = pd.to_numeric(df["G"], errors="coerce").fillna(0)
                top = df.sort_values(by="G", ascending=False).head(10)
                st.dataframe(top[["Spieler", "Team", "G"]])

            elif option == "Top-Vorbereiter":
                df["A"] = pd.to_numeric(df["A"], errors="coerce").fillna(0)
                top = df.sort_values(by="A", ascending=False).head(10)
                st.dataframe(top[["Spieler", "Team", "A"]])

        elif is_gamelog:
            st.subheader("📄 Gamelog-Datei erkannt")

            option = st.selectbox(
                "Was möchtest du analysieren?",
                ["Punkte pro Spiel", "Tore pro Spiel", "Assists pro Spiel"]
            )

            df["Year"] = df["Year"].astype(str)
            df["Datum"] = pd.to_datetime(df["Day"] + "/" + df["Year"], format="%a %d/%m/%Y", errors="coerce")
            df = df.sort_values(by="Datum")

            if option == "Punkte pro Spiel":
                df["P"] = pd.to_numeric(df["P"], errors="coerce").fillna(0)
                st.line_chart(df.set_index("Datum")["P"])

            elif option == "Tore pro Spiel":
                df["G"] = pd.to_numeric(df["G"], errors="coerce").fillna(0)
                st.line_chart(df.set_index("Datum")["G"])

            elif option == "Assists pro Spiel":
                df["A"] = pd.to_numeric(df["A"], errors="coerce").fillna(0)
                st.line_chart(df.set_index("Datum")["A"])

            st.markdown("---")
            st.subheader("📈 Streak-Auswertung")

            if st.button("Streaks berechnen"):
                with st.spinner("Berechne Streaks..."):
                    temp_file = "temp_gamelog.csv"
                    df.to_csv(temp_file, sep=";", index=False)

                    vs = lambda d: d.strftime("%Y-%m-%d") if pd.notna(d) else "?"

                    for kategorie, bezeichnung in [("P", "Punkte"), ("G", "Tore"), ("A", "Assists")]:
                        res = berechne_streaks_von_csv(temp_file, kategorie)

                        st.markdown(f"### {bezeichnung}:\n")
                        st.markdown(f"🔁 Längster {bezeichnung}-Streak: {res['max_streak']} (von {vs(res['max_streak_start'])}  {res['max_streak_start_opp']} bis {vs(res['max_streak_end'])}  {res['max_streak_end_opp']})")
                        st.markdown(f"➡️ Aktueller {bezeichnung}-Streak: {res['current_streak']}")
                        st.markdown(f"🔇 Längster ohne {bezeichnung}-Streak: {res['max_no_streak']} (von {vs(res['max_no_streak_start'])}  {res['max_no_streak_start_opp']} bis {vs(res['max_no_streak_end'])}  {res['max_no_streak_end_opp']})")
                        st.markdown(f"➡️ Aktuell ohne {bezeichnung}: {res['current_no_streak']}")

        else:
            st.error("❌ Unbekanntes Format. Bitte lade eine passende Datei hoch.")
    else:
        st.info("⬆️ Bitte lade eine CSV-Datei hoch.")

