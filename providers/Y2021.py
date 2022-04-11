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
        sections = re.split(r"Date.*Balance\s*|.*>>>\s", page.extract_text(), maxsplit=2 | re.IGNORECASE)
        if len(sections) == 3:
            transactions += parse_transactions(sections[1])  # Deposits
        else:
            continue
        # transactions["skipped_pages"].append(page.page_number)
    # transactions["used_pages"] = transactions["total_pages"] - len(transactions["skipped_pages"])
    # output["skipped_pages"] = len(SKIPPED_PAGES)
    return transactions


def parse_transactions(section: str) -> list:
    matches = re.findall(r'(\d{2}\/\d{2})\s+([a-zA-Z ]*)([\d ]*)([$\d.,]*)(\s.*)((?:\n(?!\d{2}\/\d{2}).*)*)', section)

    if not matches:
        raise ValueError('oops!')

    transactions = []
    for match in matches:
        # Skip beginning and ending balance transactions
        if str(match[1]).casefold().strip() in ["Beginning Balance".casefold(), "Ending Balance".casefold()]:
            continue
        global START_DATE
        global END_DATE
        start = datetime.strptime(START_DATE, '%m/%d/%Y')
        transaction_date = datetime.strptime(f"{match[0]}/{start.year}", '%m/%d/%Y')
        end = datetime.strptime(END_DATE, '%m/%d/%Y')

        if start <= transaction_date <= end:
            tx_date = transaction_date
        else:
            tx_date = datetime.strptime(f"{match[0]}/{end.year}", '%m/%d/%Y')
        # TODO: Convert to parameter or default year
        # Skip transactions that are not in the specified calendar year
        if tx_date.year not in [2020, 2021]:
            continue
        tx_date = tx_date.strftime('%m/%d/%Y')
        tx_type = match[1].strip()

        #TODO: Revise tx_amount grooming
        if tx_type in ["USAA DEBIT", "USAA FUNDS TRANSFER DB"]:
            tx_amount = "{:0.2f}".format(float(match[3][1:].replace(',', ''))) if match[3] else None
        else:
            tx_amount = "{:0.2f}".format(float(match[3][1:].replace(',', ''))) if match[2] else None

        tx_id = re.sub(r'[\s]+', ' ', match[2]).strip() if tx_type not in ["INTEREST PAID",
                                                                           "USAA DEBIT",
                                                                           "USAA FUNDS TRANSFER DB"] else None  # Replace all types of whitespaces with a single space
        tx_description = " ".join(re.sub(r'[\s]+', ' ', match[5]).splitlines()).strip() if match[5] else None # Replace all types of whitespaces with a single space
        tags = extract_tags(tx_description)
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
    global START_DATE
    global END_DATE
    text = pdf.extract_text()
    date_range = re.search(r"(statement period: )([\d]{2})\/([\d]{2})\/([\d]{4})[\s\D]*([\d]{2})\/([\d]{2})\/([\d]{4})",
                           text,
                           re.IGNORECASE)
    START_DATE = datetime.strptime(f"{date_range[2]}/{date_range[3]}/{date_range[4]}", '%m/%d/%Y').strftime('%m/%d/%Y')
    END_DATE = datetime.strptime(f"{date_range[5]}/{date_range[6]}/{date_range[7]}", '%m/%d/%Y').strftime('%m/%d/%Y')
    return {
        'start_date': START_DATE,
        'end_date': END_DATE
    }
