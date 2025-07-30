import streamlit as st

from sub_app import spieler_main as spieleranalyse_main
from sub_app2 import team_streak_main as teamstreak_main
from sub_app3 import team_tabelle_main as teamtabelle_main

st.set_page_config(page_title="Eishockey Analyse Tool", layout="wide")

# Seitenmenü
st.sidebar.title("📂 Navigation")
auswahl = st.sidebar.radio(
    "Wähle einen Analysebereich:",
    [
        "📊 Spieleranalyse (Gamelog)",
        "📈 Team-Streaks (Spielplan)",
        "📋 Team-Tabelle (nach Zeitraum)"
    ]
)

# Navigation zu den Modulen
if auswahl == "📊 Spieleranalyse (Gamelog)":
    spieleranalyse_main()
elif auswahl == "📈 Team-Streaks (Spielplan)":
    teamstreak_main()
elif auswahl == "📋 Team-Tabelle (nach Zeitraum)":
    teamtabelle_main()
