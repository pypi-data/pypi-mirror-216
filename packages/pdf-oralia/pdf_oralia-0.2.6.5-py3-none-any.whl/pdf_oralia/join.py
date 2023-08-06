import logging
from pathlib import Path

import pandas as pd


def extract_excel_to_dfs(directory, df_names=["charge", "locataire"]):
    p = Path(directory)
    dfs = {name: [] for name in df_names}

    for file in p.glob("*.xlsx"):
        year, month, immeuble, table = file.stem.split("_")
        df = pd.read_excel(file, dtype={"lot": str}).assign(
            annee=year, mois=month, immeuble=immeuble[:3]
        )
        dfs[table].append(df)

    return dfs


def join_excel(directory, dest, df_names=["charge", "locataire"]):
    dfs = extract_excel_to_dfs(directory, df_names)
    destinations = {}
    for tablename, datas in dfs.items():
        df = pd.concat(datas)
        destination = Path(dest) / f"{tablename}.xlsx"
        df.to_excel(destination, index=False)
        destinations[tablename] = destination
        logging.info(f"{destination} written")
    return destinations
