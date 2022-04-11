import errno
import importlib
import pdfplumber
import os
from os import listdir
from os.path import isfile, join

from common.enums import IMPORT_PROVIDER, EXPORT_FORMAT
from common.functions import print_transactions

PROJECT_DIRECTORY = os.path.dirname(os.path.realpath(__file__))
STATEMENTS_DIRECTORY = os.path.join(PROJECT_DIRECTORY, "statements")
OUTPUT_DIRECTORY = os.path.join(PROJECT_DIRECTORY, "output")

if __name__ == "__main__":
    try:
        if not os.path.exists(STATEMENTS_DIRECTORY):
            os.makedirs(STATEMENTS_DIRECTORY)
            print(f"Created STATEMENTS_DIRECTORY: {STATEMENTS_DIRECTORY}")
        else:
            print(f"Statement directory already exists: {STATEMENTS_DIRECTORY}")

        if not os.path.exists(OUTPUT_DIRECTORY):
            os.makedirs(OUTPUT_DIRECTORY)
            print(f"Created OUTPUT_DIRECTORY: {OUTPUT_DIRECTORY}")
        else:
            print(f"Output directory already exists: {OUTPUT_DIRECTORY}")

    except OSError as e:
        if e.errno != errno.EEXIST:
            raise

    statements = list(filter(lambda x: x.casefold().endswith('.pdf'), os.listdir(STATEMENTS_DIRECTORY)))

    transactions = []
    for statement in statements:
        with pdfplumber.open(f"{STATEMENTS_DIRECTORY}/{statement}") as pdf:
            provider = list(filter(lambda x: x.value in pdf.metadata["Producer"], IMPORT_PROVIDER))[0].name

            if not provider:
                raise ValueError("Provider not found")

            p = importlib.import_module(f"providers.{provider}", package=None)
            metadata = {
                'file_name': os.path.splitext(statement)[0],
                'file_extension': os.path.splitext(statement)[1],
                'file_type': os.path.splitext(statement)[1].lstrip('.').upper(),
                'full_path': f"{STATEMENTS_DIRECTORY}/{statement}",
                'total_pages': len(pdf.pages),
                'statement_range': p.parse_statement_range(pdf.pages[0])
            }
            print(metadata)
            transactions += p.extract_transactions(pdf.pages)
        print_transactions(transactions, EXPORT_FORMAT.TABLE)
