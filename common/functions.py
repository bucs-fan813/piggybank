import json

import pandas as pd
from pdfplumber import open
from importlib import import_module
from datetime import datetime
from os.path import splitext, isdir

from common.constants import Tags
from common.enums import EXPORT_FORMAT, IMPORT_PROVIDER


def is_deductible(tags: list) -> bool:
    for tag in tags:
        if tag in Tags.get_tax_deductible_tags():
            return True
    return False


def extract_tags(text: str) -> list:
    if text is None:
        return []
    tags = Tags.get_all_tags()
    for _ in tags.keys():
        return [tags[key] for key in tags.keys() if key.casefold() in text.casefold()]


def read_data(file: str, provider: str = None) -> dict:
    with open(file) as pdf:
        provider = [item.name for item in IMPORT_PROVIDER if item.name == provider]
        if not provider:
            raise ValueError("Provider not found")

        p = import_module(f"providers.{provider[0]}", package=None)
        metadata = {
            'file_name': splitext(file)[0],
            'file_extension': splitext(file)[1],
            'file_type': splitext(file)[1].lstrip('.').upper(),
            'full_path': file,
            'total_pages': len(pdf.pages),
            'statement_range': p.parse_statement_range(pdf.pages[0])
        }
        print(metadata)
        return {
            "metadata": metadata,
            "data": p.extract_transactions(pdf.pages)
        }


def print_transactions(text: str, provider=None, export_format=None, is_deductible=False, output_path=None):
    data = json.loads(json.dumps(text))
    if is_deductible is True:
        data = list(filter(lambda item: item["Tax Deductible"] is True, data))

    if export_format == EXPORT_FORMAT.JSON.casefold():
        print(data)
    elif export_format == EXPORT_FORMAT.TABLE.casefold():
        pd.set_option('display.max_rows', None)
        df = pd.DataFrame(data)
        if "Total" in df.columns:
            df = df.reindex(columns=(list([a for a in df.columns if a != 'Total'] + ['Total'])))
        if "Date" in df.columns:
            df["Date"] = pd.to_datetime(df["Date"], format='%m/%d/%Y')
            df = df.sort_values("Date", ascending=True, ignore_index=True)
        print(df)
    elif export_format == EXPORT_FORMAT.SPREADSHEET.casefold():
        if output_path is None:
            raise FileExistsError(f"You must provide an \"output_path\" parameter")
        elif not isdir(output_path):
            raise FileExistsError(f"Output path ({output_path}) does not exist")

        timestamp = f"{datetime.now():%Y%m%dT%H%M%S}"
        filename = f"{output_path}/{timestamp}.xlsx"
        df = pd.DataFrame(data)
        if "Total" in df.columns:
            df = df.reindex(columns=(list([a for a in df.columns if a != 'Total'] + ['Total'])))

        # Create a Pandas Excel writer using XlsxWriter as the engine.
        writer = pd.ExcelWriter(filename, engine="xlsxwriter", engine_kwargs={'options': {'strings_to_numbers': True}})
        pd.DataFrame(df).to_excel(writer, sheet_name=timestamp)
        writer.save()
        print(f"Created: {filename}")
