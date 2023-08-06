import logging
from logging.config import dictConfig
from pathlib import Path

import click

from .extract import extract_save

logging_config = dict(
    version=1,
    formatters={"f": {"format": "%(levelname)-8s %(name)-12s %(message)s"}},
    handlers={
        "h": {
            "class": "logging.StreamHandler",
            "formatter": "f",
            "level": logging.DEBUG,
        }
    },
    root={
        "handlers": ["h"],
        "level": logging.DEBUG,
    },
)

dictConfig(logging_config)


@click.group()
def main():
    pass


@main.group()
def extract():
    pass


@extract.command()
@click.argument("pdf_file", required=1)
@click.option("--dest", help="Où mettre les fichiers produits", default="")
def on(pdf_file, dest):
    if not dest:
        pdf_path = Path(pdf_file)
        dest = pdf_path.parent

    extract_save(pdf_file, dest)


@extract.command()
@click.option("--src", help="Tous les fichiers dans folder", default="./")
@click.option("--dest", help="Où mettre les fichiers produits", default="./")
def all(src, dest):
    p = Path(src)

    d = Path(dest)
    d.mkdir(exist_ok=True)

    pdf_files = [x for x in p.iterdir() if ".pdf" in str(x)]
    for pdf_file in pdf_files:
        logging.info(f"Found {pdf_file}")
        extract_save(pdf_file, d)


@main.command()
@click.option("--src", help="Tous les fichiers dans src", default="./")
@click.option("--dest", help="Où mettre les fichiers produits", default="")
def join(src, dest):
    join_excel(src, dest, df_names=["charge", "locataire"])
