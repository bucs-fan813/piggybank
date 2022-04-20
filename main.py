import argparse
import errno
from os import listdir, makedirs
from os.path import join, exists, dirname, realpath
from distutils.util import strtobool

from common.enums import EXPORT_FORMAT, EXPORT_PERIOD, IMPORT_PROVIDER
from common.functions import print_transactions, read_data

PROJECT_DIRECTORY = dirname(realpath(__file__))
STATEMENTS_DIRECTORY = join(PROJECT_DIRECTORY, "statements")
OUTPUT_DIRECTORY = join(PROJECT_DIRECTORY, "output")
period = EXPORT_PERIOD.ALL
transactions = []

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Seed cases and workflow stages through endpoints")
    parser.add_argument('--output',
                        type=str,
                        default=EXPORT_FORMAT.TABLE,
                        help="Print data to stdout or save to file")
    parser.add_argument('--provider',
                        type=str,
                        default=None,
                        help="Specify the service provider name and version")
    parser.add_argument('--is_deductible',
                        default=False,
                        help="Filter tax deductible transactions")

    args = parser.parse_args()

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
    statements = list(map(lambda file: read_data(file, args.provider), files))
    is_deductible = bool(strtobool(args.is_deductible))
    if period == EXPORT_PERIOD.STATEMENT:
        for statement in statements:
            print_transactions(statement["data"], EXPORT_FORMAT.TABLE)
    else:
        for statement in statements:
            transactions += statement["data"]
        print_transactions(transactions, provider=args.provider, export_format=args.output.casefold(), is_deductible=is_deductible, output_path=OUTPUT_DIRECTORY)
