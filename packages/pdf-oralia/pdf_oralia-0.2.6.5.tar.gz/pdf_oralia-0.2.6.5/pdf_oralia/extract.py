import logging
from datetime import datetime
from pathlib import Path

import pandas as pd
import pdfplumber

from .extract_charge import extract_charge, extract_remise_com
from .extract_locataire import extract_situation_loc

charge_table_settings = {
    "vertical_strategy": "lines",
    "horizontal_strategy": "text",
}


def extract_date(page_text):
    """Extract date from a page

    :param page_text: text in the page
    :return: the extracted date
    """
    blocs = page_text.split("\n")
    for b in blocs:
        if "Lyon le" in b:
            words = b.split(" ")
            return datetime.strptime(words[-1], "%d/%m/%Y")


def extract_from_pdf(pdf, charge_dest, location_dest):
    """Build charge_dest and location_dest xlsx file from pdf"""
    loc_tables = []
    charge_table = []

    df_1st_charge = extract_remise_com(
        pdf.pages[0].extract_table(charge_table_settings)
    )

    for page in pdf.pages[1:]:
        page_text = page.extract_text()
        situation_loc_line = [
            l for l in page_text.split("\n") if "SITUATION DES LOCATAIRES" in l
        ]
        date = extract_date(page_text)
        mois = date.strftime("%m")
        annee = date.strftime("%Y")
        if situation_loc_line:
            # mois, annee = situation_loc_line[0].split(" ")[-2:]
            if loc_tables:
                loc_tables.append(page.extract_table()[1:])
            else:
                loc_tables.append(page.extract_table())

        elif "RECAPITULATIF DES OPERATIONS" in page_text:
            if charge_table:
                charge_table += page.extract_table(charge_table_settings)[1:]
            else:
                charge_table = page.extract_table(charge_table_settings)

    df_charge = extract_charge(charge_table)
    df_charge_with_1st = pd.concat([df_1st_charge, df_charge])
    df_charge_with_1st.to_excel(charge_dest, sheet_name="Charges", index=False)
    logging.info(f"{charge_dest} saved")

    df_loc = extract_situation_loc(loc_tables, mois=mois, annee=annee)
    df_loc = df_loc.assign()
    df_loc.to_excel(location_dest, sheet_name="Location", index=False)
    logging.info(f"{location_dest} saved")


def extract_save(pdf_file, dest):
    """Extract charge and locataire for pdf_file and put xlsx file in dest"""
    pdf_file = Path(pdf_file)
    xls_charge = Path(dest) / f"{pdf_file.stem.replace(' ', '_')}_charge.xlsx"
    xls_locataire = Path(dest) / f"{pdf_file.stem.replace(' ', '_')}_locataire.xlsx"

    pdf = pdfplumber.open(pdf_file)
    extract_from_pdf(pdf, xls_charge, xls_locataire)
