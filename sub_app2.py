import streamlit as st
import pandas as pd
from team_streak_tools import berechne_team_streaks

def team_streak_main():
    st.title("🏒 Team-Streak Analyse")

    uploaded_file = st.file_uploader("Wähle eine CSV-Datei mit Spielplan", type="csv")

    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file, delimiter=";")

        # 📅 Phasen definieren
        df["Phase"] = df["Phase"].fillna("")
        df["Phase"] = df["Phase"].astype(str)

        phase_mapping = {
            "Regular Season": "Regular Season",
            "Play-In Round 1": "Play-In",
            "Play-In Round 2": "Play-In",
            "Playoff 1/4 Final": "Playoffs",
            "Playoff 1/2 Final": "Playoffs",
            "Playoff Final": "Playoffs",
            "Playout Final": "Playout Final",
            "League Qualification": "League Qualification"
        }

        df["Phase_Kategorie"] = df["Phase"].map(phase_mapping).fillna(df["Phase"])
        alle_phasen = sorted(df["Phase_Kategorie"].unique())

        ausgewaehlte_phasen = st.multiselect("🔎 Wähle Phase(n)", alle_phasen, default=alle_phasen)

        # Nach Phase filtern
        df = df[df["Phase_Kategorie"].isin(ausgewaehlte_phasen)]

        teams = sorted(pd.unique(df["Home"].tolist() + df["Away"].tolist()))
        teamname = st.selectbox("Wähle ein Team", teams)

        if teamname:
            result = berechne_team_streaks(df, teamname)

            def vs(d):
                return d.strftime("%Y-%m-%d") if pd.notnull(d) else "?"

            st.markdown(f"### 🟢 Siege")
            st.markdown(f"🔁 **Längste Siegesserie**: {result['max_winstreak']} (von {vs(result['max_winstreak_start'])} bis {vs(result['max_winstreak_end'])})")
            st.markdown(f"➡️ **Aktuell**: {result['current_winstreak']}")

            st.markdown("---")

            st.markdown(f"### 🔴 Ohne Sieg")
            st.markdown(f"🔇 **Längste Serie ohne Sieg**: {result['max_nowin_streak']} (von {vs(result['max_nowin_streak_start'])} bis {vs(result['max_nowin_streak_end'])})")
            st.markdown(f"➡️ **Aktuell ohne**: {result['current_nowin_streak']}")
