import pdfplumber
import re

from typing import List
from datetime import datetime
from common.functions import extract_tags, isDeductable

START_DATE = ""
END_DATE = ""


def extract_transactions(pages: List[pdfplumber.page.Page]) -> list:
    transactions = []

    for page in pages:
        if re.search(f"DEPOSITS AND OTHER CREDITS|OTHER DEBITS|Beginning Balance|.*>>>$", page.extract_text()):
            sections = re.split(patterns, page.extract_text())
            if len(sections) == 2:
                transactions += parse_transactions(sections[1])  # Deposits
            elif len(sections) == 3:
                transactions += parse_transactions(sections[1])  # Deposits
                transactions += parse_transactions(sections[2])  # Expenses
        else:
            continue
            # transactions["skipped_pages"].append(page.page_number)
    # transactions["used_pages"] = transactions["total_pages"] - len(transactions["skipped_pages"])
    # output["skipped_pages"] = len(SKIPPED_PAGES)
    return transactions


def parse_transactions(section: str) -> list:
    matches = re.findall(r'(\d{2}\/\d{2})(\s*)([0-9.,]*)([A-Z ]+[A-Z])(.*)([\r\n])?(?!\d{2}\/\d{2})(.*)', section)
    if not matches:
        raise ValueError('oops!')
    transactions = []
    for match in matches:
        global START_DATE
        global END_DATE
        start = datetime.strptime(START_DATE, '%m/%d/%Y')
        transaction_date = datetime.strptime(f"{match[0]}/{start.year}", '%m/%d/%Y')
        end = datetime.strptime(END_DATE, '%m/%d/%Y')
        if start <= transaction_date <= end:
            tx_date = transaction_date
        else:
            tx_date = datetime.strptime(f"{match[0]}/{end.year}", '%m/%d/%Y')

        if tx_date.year not in [2020, 2021]:
            continue
        tx_date = tx_date.strftime('%m/%d/%Y')
        tx_amount = "{:0.2f}".format(float(match[2].replace(',', '')))
        tx_type = match[3].strip()
        tx_id = re.sub(r'[\s]+', ' ', match[4]).strip()  # Replace all types of whitespaces with a single space
        tx_description = re.sub(r'[\s]+', ' ', match[6]).strip()  # Replace all types of whitespaces with a single space
        tags = extract_tags(tx_description)
        # if tx_type in ["USAA FUNDS TRANSFER DB","ATM DB NONLOCAL"]: continue
        tx_deductible = isDeductable(tags)
        transactions.append({
            "Date": tx_date,
            "Amount": tx_amount,
            "Type": tx_type,
            "Transaction ID": tx_id,
            "Description": tx_description,
            "Tax Deductible": tx_deductible,
            "Category": tags
        })
    return transactions


def parse_statement_range(pdf: pdfplumber.page.Page) -> dict:
    statement_table = pdf.extract_tables()
    date_range = statement_table[0][1:][0][2].split(' - ')
    global START_DATE
    global END_DATE
    START_DATE = datetime.strptime(f"{date_range[0]}", '%m/%d/%y').strftime('%m/%d/%Y')
    END_DATE = datetime.strptime(f"{date_range[1]}", '%m/%d/%y').strftime('%m/%d/%Y')
    return {
        'start_date': START_DATE,
        'end_date': END_DATE
    }
