import pdfplumber
import json
import re
import os, errno
import pandas as pd

from datetime import datetime
from enums import EXPORT_FORMAT
from constants import *
from os import listdir
from os.path import isfile, join

PROJECT_DIRECTORY = os.path.dirname(os.path.realpath(__file__))
STATEMENTS_DIRECTORY = os.path.join(PROJECT_DIRECTORY, "statements")

def extract_transactions(text:str) -> list:
    transactions = []
    matches = re.findall(r'(\d{2}\/\d{2})(\s*)([0-9.,]*)([A-Z ]+[A-Z])(.*)([\r\n]+([^\r\n]+))?', text)
    
    if matches:
        for match in matches:
            transactions.append({
                "date" : datetime.strptime(f"{match[0]}/2020", '%m/%d/%Y').strftime('%m/%d/%Y'),
                "amount" : "{:0.2f}".format(float(match[2].replace(',',''))),
                "type" : match[3].strip(),
                "txid" : re.sub(r'[\s]+', ' ', match[4]).strip(), # Replace all types of whitespaces with a single space
                "description" : re.sub(r'[\s]+', ' ', match[5]).strip() # Replace all types of whitespaces with a single space
            })
    return transactions

def print_transactions(input, export_format=None):
    if export_format == EXPORT_FORMAT.JSON:
        return json.dumps(input)
    elif export_format == EXPORT_FORMAT.TABLE:
        return pd.DataFrame(json.loads(json.dumps(input)))
    
    return input

if __name__ == "__main__":
    try:
        os.makedirs(STATEMENTS_DIRECTORY)
        print(f"Created STATEMENTS_DIRECTORY: {STATEMENTS_DIRECTORY}")
    except OSError as e:
        if e.errno != errno.EEXIST:
            raise
        print(f"Statement directory already exists: {STATEMENTS_DIRECTORY}")

    statements = [f for f in listdir(STATEMENTS_DIRECTORY) if isfile(join(STATEMENTS_DIRECTORY, f))]
    for statement in statements:
        with pdfplumber.open(f"{STATEMENTS_DIRECTORY}/{statement}") as pdf:
            DEPOSITS = []
            OTHER = []
            RESULTS = []
            SKIPPED_PAGES = []
            STATEMENT_START = ''
            STATEMENT_END = ''

            for page in pdf.pages:
                if re.search(patterns, page.extract_text()):
                    sections = re.split(patterns, page.extract_text())
                    if len(sections) == 2:
                        OTHER += extract_transactions(sections[1])
                    elif len(sections) == 3:
                        DEPOSITS += extract_transactions(sections[1])
                        OTHER += extract_transactions(sections[2])
                else:
                    SKIPPED_PAGES.append(page.page_number)
        output = {
            'file_name' : os.path.splitext(statement)[0],
            'file_extention' : os.path.splitext(statement)[1],
            'file_type' : os.path.splitext(statement)[1].lstrip('.').upper(),
            'full_path' : f"{STATEMENTS_DIRECTORY}/{statement}",
            'total_pages' : len(pdf.pages),
            'used_pages' : len(pdf.pages) - len(SKIPPED_PAGES),
            'skipped_pages' : len(SKIPPED_PAGES)
        }
        
    print(print_transactions(DEPOSITS, EXPORT_FORMAT.TABLE))
    print(print_transactions(OTHER, EXPORT_FORMAT.TABLE))