import xlsxwriter
import json
import os
import pdfplumber
import importlib

import pandas as pd
from datetime import datetime

from common.constants import Tags
from common.enums import EXPORT_FORMAT, EXPORT_PERIOD, IMPORT_PROVIDER

PROJECT_DIRECTORY = os.path.dirname(os.path.realpath(__file__))
OUTPUT_DIRECTORY = os.path.abspath(os.path.join(PROJECT_DIRECTORY, os.pardir))
OUTPUT_DIRECTORY = os.path.join(OUTPUT_DIRECTORY, "output")


def is_deductible(text: str) -> bool:
    return False


def extract_tags(text: str) -> list:
    if text is None:
        return []
    tags = Tags.get_tags()
    for _ in tags.keys():
        return [tags[key] for key in tags.keys() if key.casefold() in text.casefold()]


def read_data(file: str) -> dict:
    data = []
    with pdfplumber.open(file) as pdf:
        provider = list(filter(lambda x: x.value in pdf.metadata["Producer"], IMPORT_PROVIDER))[0].name

        if not provider:
            raise ValueError("Provider not found")

        p = importlib.import_module(f"providers.{provider}", package=None)
        metadata = {
            'file_name': os.path.splitext(file)[0],
            'file_extension': os.path.splitext(file)[1],
            'file_type': os.path.splitext(file)[1].lstrip('.').upper(),
            'full_path': file,
            'total_pages': len(pdf.pages),
            'statement_range': p.parse_statement_range(pdf.pages[0])
        }
        print(metadata)
        return {
            "metadata": metadata,
            "data": p.extract_transactions(pdf.pages)
        }


def print_transactions(text: str, export_format=None):
    data = json.loads(json.dumps(text))
    if export_format == EXPORT_FORMAT.JSON:
        print(data)
    elif export_format == EXPORT_FORMAT.TABLE:
        pd.set_option('display.max_rows', None)
        print(pd.DataFrame(data))
    elif export_format == EXPORT_FORMAT.CSV:
        # Create a Pandas Excel writer using XlsxWriter as the engine.
        sheet_name = data[0]["tx_date"][-4:]
        timestamp = f"{datetime.now():%Y%m%dT%H%M%S}"
        filename = f"{OUTPUT_DIRECTORY}/{timestamp}.xlsx"
        writer = pd.ExcelWriter(filename, engine='xlsxwriter')
        pd.DataFrame(data).to_excel(writer, sheet_name=sheet_name)
        writer.save()
        print(f"Created: {filename}")
