import logging

import pandas as pd


def parse_above_loc(content):
    row = {}
    app, loc, *_ = content.split("\n")
    app_ = app.split(" ")
    row["lot"] = f"{int(app_[1]):02d}"
    row["type"] = " ".join(app_[2:])
    row["locataire"] = loc
    return pd.Series(row)


def join_row(last, next):
    row = []
    for i in range(len(last)):
        if last[i] and next[i]:
            row.append(f"{last[i]}\n{next[i]}")
        elif last[i]:
            row.append(last[i])
        elif next[i]:
            row.append(next[i])
        else:
            row.append("")
    return row


def join_tables(tables):

    joined = tables[0]

    for t in tables[1:]:
        last_row = joined[-1]
        if "Totaux" not in last_row[0]:
            first_row = t[0]
            joined_row = join_row(last_row, first_row)
            joined = joined[:-1] + [joined_row] + t[1:]
        else:
            joined += t

    return joined


def extract_situation_loc(tables, mois, annee):
    """From pdfplumber table extract locataire df"""
    table = join_tables(tables)
    try:
        df = pd.DataFrame(table[1:], columns=table[0])
    except IndexError:
        print(table)
    rows = []
    for i, row in df[df["Locataires"] == "Totaux"].iterrows():
        above_row_loc = df.iloc[i - 1]["Locataires"]
        up_row = pd.concat(
            [
                row,
                parse_above_loc(above_row_loc),
            ]
        )

        rows.append(up_row)
    df_cleaned = pd.concat(rows, axis=1).T
    df_cleaned.drop(["Locataires", "", "Période"], axis=1, inplace=True)

    df_cleaned = df_cleaned.astype(
        {
            "Loyers": "float64",
            "Taxes": "float64",
            "Provisions": "float64",
            "Divers": "float64",
            "Total": "float64",
            "Réglés": "float64",
            "Impayés": "float64",
        },
        errors="ignore",
    )

    df_cleaned = df_cleaned.assign(mois=mois, annee=annee)
    return df_cleaned
