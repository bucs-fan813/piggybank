import pdfplumber
import json
import re
import os, errno
import xlsxwriter
import pandas as pd

from datetime import datetime
from enums import EXPORT_FORMAT
from constants import Tags, Patterns
from os import listdir
from os.path import isfile, join

PROJECT_DIRECTORY = os.path.dirname(os.path.realpath(__file__))
STATEMENTS_DIRECTORY = os.path.join(PROJECT_DIRECTORY, "statements")
OUTPUT_DIRECTORY = os.path.join(PROJECT_DIRECTORY, "output")

START_DATE = None
END_DATE = None

def extract_transactions(text:str) -> list:
    transactions = []
    matches = re.findall(r'(\d{2}\/\d{2})(\s*)([0-9.,]*)([A-Z ]+[A-Z])(.*)([\r\n])?(?!\d{2}\/\d{2})(.*)', text)
    
    if matches:
        for match in matches:
            global START_DATE
            global END_DATE
            start = datetime.strptime(START_DATE, '%m/%d/%Y')
            transaction_date = datetime.strptime(f"{match[0]}/{start.year}", '%m/%d/%Y')
            end = datetime.strptime(END_DATE, '%m/%d/%Y')
            if (start <= transaction_date <= end):
                tx_date = transaction_date
            else:
                tx_date = datetime.strptime(f"{match[0]}/{end.year}", '%m/%d/%Y')
            
            if tx_date.year != 2020:
                continue
            tx_date = tx_date.strftime('%m/%d/%Y')
            tx_amount = "{:0.2f}".format(float(match[2].replace(',','')))
            tx_type = match[3].strip()
            tx_id = re.sub(r'[\s]+', ' ', match[4]).strip() # Replace all types of whitespaces with a single space
            tx_description = re.sub(r'[\s]+', ' ', match[6]).strip() # Replace all types of whitespaces with a single space
            tags = extract_tags(tx_description)
            if tx_type in ["USAA FUNDS TRANSFER DB","ATM DB NONLOCAL"]: continue
            tx_isDeductable = isDeductable(tx_description)
            transactions.append({
                "tx_date" : tx_date,
                "tx_amount" : tx_amount,
                "tx_type" : tx_type,
                "tx_id" : tx_id,
                "tx_description" : tx_description,
                "tx_isDeductable" : tx_isDeductable,
                "tags" : tags
            })
    return transactions

def isDeductable(text:str) -> bool:
    return False

def extract_tags(text:str) -> str:
    tags = Tags.getTags()
    for key in tags.keys():
        return [tags[key] for key in tags.keys() if key.casefold() in text.casefold()]

def print_transactions(input, export_format=None):
    if export_format == EXPORT_FORMAT.JSON:
        return json.dumps(input)
    elif export_format == EXPORT_FORMAT.TABLE:
        pd.set_option('display.max_rows', None)
        return pd.DataFrame(json.loads(json.dumps(input)))
    elif export_format == EXPORT_FORMAT.CSV:
        # Create a Pandas Excel writer using XlsxWriter as the engine.
        timestamp = f"{datetime.now():%Y%m%dT%H%M%S}"
        writer = pd.ExcelWriter(f"{OUTPUT_DIRECTORY}/{timestamp}.xlsx", engine='xlsxwriter')
        pd.DataFrame(json.loads(json.dumps(input))).to_excel(writer,sheet_name='2020')
        writer.save()
        return
    return input

def parse_statement_range(pdf:pdfplumber.page.Page) -> dict:
    statement_table = pdf.extract_tables()
    date_range = statement_table[0][1:][0][2].split(' - ')
    global START_DATE
    global END_DATE
    START_DATE = datetime.strptime(f"{date_range[0]}", '%m/%d/%y').strftime('%m/%d/%Y')
    END_DATE =  datetime.strptime(f"{date_range[1]}", '%m/%d/%y').strftime('%m/%d/%Y')
    return {
        'start_date' : START_DATE,
        'end_date' : END_DATE
    }

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
        
    EXPENSES = []
    DEPOSITS = []
    patterns = Patterns.getSectionPatterns()
    statements = [f for f in listdir(STATEMENTS_DIRECTORY) if not f.startswith(".") and isfile(join(STATEMENTS_DIRECTORY, f))]
    for statement in statements:
        with pdfplumber.open(f"{STATEMENTS_DIRECTORY}/{statement}") as pdf:
            SKIPPED_PAGES = []
            output = {
            'file_name' : os.path.splitext(statement)[0],
            'file_extention' : os.path.splitext(statement)[1],
            'file_type' : os.path.splitext(statement)[1].lstrip('.').upper(),
            'full_path' : f"{STATEMENTS_DIRECTORY}/{statement}",
            'total_pages' : len(pdf.pages),
            'statement_range' : parse_statement_range(pdf.pages[0])
            }            
            for page in pdf.pages:
                if re.search(patterns, page.extract_text()):
                    sections = re.split(patterns, page.extract_text())
                    if len(sections) == 2:
                        EXPENSES += extract_transactions(sections[1])
                    elif len(sections) == 3:
                        DEPOSITS += extract_transactions(sections[1])
                        EXPENSES += extract_transactions(sections[2])
                else:
                    SKIPPED_PAGES.append(page.page_number)

            output["used_pages"] = len(pdf.pages) - len(SKIPPED_PAGES)
            output["skipped_pages"] = len(SKIPPED_PAGES)
        print(output)
    print(print_transactions(EXPENSES, EXPORT_FORMAT.CSV))