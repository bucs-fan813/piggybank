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
        if tag in Tags.get_tax_deductable_tags():
            return True
    return False


def extract_tags(text: str) -> list:
    if text is None:
        return []
    tags = Tags.get_all_tags()
    for _ in tags.keys():
        return [tags[key] for key in tags.keys() if key.casefold() in text.casefold()]


def read_data(file: str) -> dict:
    with open(file) as pdf:
        provider = list(filter(lambda x: x.value in pdf.metadata["Producer"], IMPORT_PROVIDER))[0].name

        if not provider:
            raise ValueError("Provider not found")

        p = import_module(f"providers.{provider}", package=None)
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


def print_transactions(text: str, export_format=None, output_path=None):
    data = json.loads(json.dumps(text))
    if export_format == EXPORT_FORMAT.JSON:
        print(data)
    elif export_format == EXPORT_FORMAT.TABLE:
        pd.set_option('display.max_rows', None)
        print(pd.DataFrame(data))
    elif export_format == EXPORT_FORMAT.CSV:
        if output_path is None:
            raise FileExistsError(f"You must provide an \"output_path\" parameter")
        elif not isdir(output_path):
            raise FileExistsError(f"Output path ({output_path}) does not exist")

        sheet_name = data[0]["Date"][-4:]
        timestamp = f"{datetime.now():%Y%m%dT%H%M%S}"
        filename = f"{output_path}/{timestamp}.xlsx"

        # Create a Pandas Excel writer using XlsxWriter as the engine.
        writer = pd.ExcelWriter(filename, engine="xlsxwriter")
        pd.DataFrame(data).to_excel(writer, sheet_name=sheet_name)
        writer.save()
        print(f"Created: {filename}")
