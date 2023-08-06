import re

import numpy as np
import pandas as pd

RECAPITULATIF_DES_OPERATION = 1


def is_it(page_text):
    if (
        "RECAPITULATIF DES OPERATIONS" in page_text
        and "COMPTE RENDU DE GESTION" not in page_text
    ):
        return True
    return False


def get_lot(txt):
    """Return lot number from "RECAPITULATIF DES OPERATIONS" """
    regex = r"[BSM](\d+)\s-"
    result = re.findall(regex, txt)
    if result:
        return "{:02d}".format(int(result[0]))
    return "*"


def keep_row(row):
    return not any(
        [
            word.lower() in row[RECAPITULATIF_DES_OPERATION].lower()
            for word in ["TOTAL", "TOTAUX", "Solde créditeur", "Solde débiteur"]
        ]
    )


def extract(table, additionnal_fields: dict = {}):
    """Turn table to dictionary with additionnal fields"""
    extracted = []
    header = table[0]
    for row in table[1:]:
        if keep_row(row):
            r = dict()
            for i, value in enumerate(row):
                if header[i] == "":
                    r["Fournisseur"] = value
                else:
                    r[header[i]] = value

            for k, v in additionnal_fields.items():
                r[k] = v

            r["lot"] = get_lot(row[RECAPITULATIF_DES_OPERATION])

            if "honoraire" in row[RECAPITULATIF_DES_OPERATION]:
                r["Fournisseur"] = "IMI GERANCE"

            extracted.append(r)

    return extracted


def table2df(tables):
    dfs = []
    for table in tables:
        df = (
            pd.DataFrame.from_records(table)
            .replace("", np.nan)
            .dropna(subset=["Débits", "Crédits"], how="all")
        )
        df["Fournisseur"] = df["Fournisseur"].fillna(method="ffill")
        dfs.append(df)
    return pd.concat(dfs)
