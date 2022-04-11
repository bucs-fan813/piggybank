import errno
from os import listdir, makedirs
from os.path import join, exists, dirname, realpath

from common.enums import EXPORT_FORMAT, EXPORT_PERIOD
from common.functions import print_transactions, read_data

PROJECT_DIRECTORY = dirname(realpath(__file__))
STATEMENTS_DIRECTORY = join(PROJECT_DIRECTORY, "statements")
OUTPUT_DIRECTORY = join(PROJECT_DIRECTORY, "output")
period = EXPORT_PERIOD.ALL
transactions = []

if __name__ == "__main__":
    try:
        if not exists(STATEMENTS_DIRECTORY):
            makedirs(STATEMENTS_DIRECTORY)
            print(f"Created STATEMENTS_DIRECTORY: {STATEMENTS_DIRECTORY}")
        else:
            print(f"Statement directory already exists: {STATEMENTS_DIRECTORY}")

        if not exists(OUTPUT_DIRECTORY):
            makedirs(OUTPUT_DIRECTORY)
            print(f"Created OUTPUT_DIRECTORY: {OUTPUT_DIRECTORY}")
        else:
            print(f"Output directory already exists: {OUTPUT_DIRECTORY}")

    except OSError as e:
        if e.errno != errno.EEXIST:
            raise

    files = list(filter(lambda file: file.casefold().endswith('.pdf'), listdir(STATEMENTS_DIRECTORY)))
    files = list(map(lambda file: f"{STATEMENTS_DIRECTORY}/{file}", files))
    statements = list(map(lambda file: read_data(file), files))

    if period == EXPORT_PERIOD.STATEMENT:
        for statement in statements:
            print_transactions(statement["data"], EXPORT_FORMAT.TABLE)
    else:
        for statement in statements:
            transactions += statement["data"]
        print_transactions(transactions, EXPORT_FORMAT.CSV, output_path=OUTPUT_DIRECTORY)
