import xlsxwriter
import json
import os
import pandas as pd
from datetime import datetime

from common.constants import Tags
from common.enums import EXPORT_FORMAT

PROJECT_DIRECTORY = os.path.dirname(os.path.realpath(__file__))
OUTPUT_DIRECTORY = os.path.abspath(os.path.join(PROJECT_DIRECTORY, os.pardir))
OUTPUT_DIRECTORY = os.path.join(OUTPUT_DIRECTORY, "output")


def isDeductable(text: str) -> bool:
    return False


def extract_tags(text: str) -> list:
    if text is None:
        return []
    tags = Tags.get_tags()
    for _ in tags.keys():
        return [tags[key] for key in tags.keys() if key.casefold() in text.casefold()]


def print_transactions(text, export_format=None):
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