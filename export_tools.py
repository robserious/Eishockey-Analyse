import csv
import pandas as pd

def exportiere_spieler_excel(spieler_liste, dateiname):
    df = pd.DataFrame(spieler_liste)
    df.to_excel(dateiname, index=False, engine="openpyxl")
    print(f"✅ Excel-Export erfolgreich: {dateiname}")

def exportiere_spieler_liste(spieler_liste, dateiname):
    with open(dateiname, "w", encoding="utf-8-sig", newline="") as datei:
        felder = ["name", "punkte", "tore", "assists", "team", "position"]
        writer = csv.DictWriter(datei, fieldnames=felder)
        writer.writeheader()
        for spieler in spieler_liste:
            writer.writerow(spieler)
    print(f"Export erfolgreich: {dateiname}")

def frage_nach_export(spieler_liste):
    if not spieler_liste:
        return
    export = input("\nMöchtest du diese Liste exportieren? (j/n): ").lower()
    if export == "j":
        typ = input("Als CSV oder Excel exportieren? (csv/xlsx): ").lower()
        dateiname = input("Dateiname (ohne Endung): ")
        if typ == "xlsx":
            exportiere_spieler_excel(spieler_liste, dateiname + ".xlsx")
        else:
            exportiere_spieler_liste(spieler_liste, dateiname + ".csv")
