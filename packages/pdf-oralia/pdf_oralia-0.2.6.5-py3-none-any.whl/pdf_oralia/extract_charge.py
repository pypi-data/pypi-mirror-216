import logging

import numpy as np
import pandas as pd


def get_lot(x):
    """Return lot number from "RECAPITULATIF DES OPERATIONS" """
    if x[:2].isdigit():
        return x[:2]
    if x[:1].isdigit():
        return "0" + x[:1]
    if x[:2] == "PC":
        return "PC"
    return ""


def extract_charge(table):
    """From pdfplumber table extract the charge dataframe"""
    df = (
        pd.DataFrame(table[1:], columns=table[0])
        .replace("", np.nan)
        .dropna(subset=["Débits", "Crédits"], how="all")
    )

    drop_index = df[
        df["RECAPITULATIF DES OPERATIONS"].str.contains("TOTAUX", case=False)
        | df["RECAPITULATIF DES OPERATIONS"].str.contains("Solde créditeur", case=False)
        | df["RECAPITULATIF DES OPERATIONS"].str.contains("Solde débiteur", case=False)
        | df["RECAPITULATIF DES OPERATIONS"].str.contains(
            "Total des reglements locataires", case=False
        )
    ].index
    df.drop(drop_index, inplace=True)

    df[""].mask(
        df["RECAPITULATIF DES OPERATIONS"].str.contains("honoraires", case=False),
        "IMI GERANCE",
        inplace=True,
    )

    df = df.assign(lot=df["RECAPITULATIF DES OPERATIONS"].map(get_lot))

    df = df.astype(
        {
            "Débits": "float64",
            "Crédits": "float64",
            "Dont T.V.A.": "float64",
            "Locatif": "float64",
            "Déductible": "float64",
        }
    )

    df.columns.values[0] = "Fournisseur"
    return df


def extract_remise_com(table):
    """Extract "remise commercial" from first page"""
    df = pd.DataFrame(table[1:], columns=table[0]).replace("", np.nan)
    df = df[
        df["RECAPITULATIF DES OPERATIONS"].str.contains(
            "Remise commerciale gérance", case=False, na=False
        )
    ]

    df.columns.values[0] = "Fournisseur"
    return df
