import pandas as pd


def is_it(page_text):
    if "SITUATION DES LOCATAIRES" in page_text:
        return True
    return False


def is_drop(row):
    if "totaux" in row[0].lower():
        return True
    if not any(row):
        return True
    return False


def extract(table, additionnal_fields: dict = {}):
    """Turn table to dictionary with additionnal fields"""
    extracted = []
    header = table[0]
    for row in table[1:]:
        if not is_drop(row):
            r = dict()
            for i, value in enumerate(row):
                if header[i] != "":
                    r[header[i]] = value
            for k, v in additionnal_fields.items():
                r[k] = v
            extracted.append(r)
    return extracted


def join_row(last, next):
    row = {}
    for key in last:
        if last[key] == next[key]:
            row[key] = last[key]
        elif last[key] and next[key]:
            row[key] = f"{last[key]}\n{next[key]}"
        elif last[key]:
            row[key] = last[key]
        elif next[key]:
            row[key] = next[key]
        else:
            row[key] = ""
    return row


def join_tables(tables):
    joined = tables[0]

    for t in tables[1:]:
        last_row = joined[-1]
        if "totaux" not in last_row["Locataires"].lower():
            first_row = t[0]
            joined_row = join_row(last_row, first_row)
            joined = joined[:-1] + [joined_row] + t[1:]
        else:
            joined += t

    return joined


def parse_lot(string):
    words = string.split(" ")
    return {"Lot": "{:02d}".format(int(words[1])), "Type": " ".join(words[2:])}


def join_row(table):
    joined = []
    for row in table:
        if row["Locataires"].startswith("Lot"):
            row.update(parse_lot(row["Locataires"]))
            row["Locataires"] = ""
            joined.append(row)
        elif row["Locataires"] == "Rappel de Loyer":
            last_row = joined[-1]
            row.update(
                {
                    "Lot": last_row["Lot"],
                    "Type": last_row["Type"],
                    "Locataires": last_row["Locataires"],
                    "Divers": "Rappel de Loyer",
                }
            )
            joined.append(row)

        elif row["Locataires"]:
            last_row = joined.pop()
            row_name = row["Locataires"].replace("\n", " ")
            row.update({k: v for k, v in last_row.items() if v})
            row["Locataires"] = last_row["Locataires"] + " " + row_name
            joined.append(row)

        else:
            if row["Période"].startswith("Solde"):
                last_row = joined.pop()
                row.update(
                    {
                        "Lot": last_row["Lot"],
                        "Type": last_row["Type"],
                        "Locataires": last_row["Locataires"],
                    }
                )
                joined.append(row)

            elif row["Période"].startswith("Du"):
                last_row = joined[-1]
                row.update(
                    {
                        "Lot": last_row["Lot"],
                        "Type": last_row["Type"],
                        "Locataires": last_row["Locataires"],
                    }
                )
                joined.append(row)
            else:
                print(row)

    return joined


def flat_tables(tables):
    tables_flat = []
    for table in tables:
        tables_flat.extend(table)
    return tables_flat


def table2df(tables):
    tables = flat_tables(tables)
    joined = join_row(tables)
    return pd.DataFrame.from_records(joined)
