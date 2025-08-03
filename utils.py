import pandas as pd
import csv
import io

def read_csv_with_delimiter_detection(uploaded_file):
    """
    Liest eine CSV-Datei mit automatischer Delimiter-Erkennung (; oder ,).
    Gibt ein pandas DataFrame zurück.
    """
    content = uploaded_file.getvalue().decode("utf-8", errors="ignore")
    sniffer = csv.Sniffer()

    try:
        dialect = sniffer.sniff(content[:1024])
        delimiter = dialect.delimiter
    except csv.Error:
        delimiter = ";"  # Fallback

    df = pd.read_csv(io.StringIO(content), delimiter=delimiter)
    return df
