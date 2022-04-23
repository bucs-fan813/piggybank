import re

from pdfplumber import page
from typing import List
from datetime import datetime

from common.functions import extract_tags, is_deductible

START_DATE = ""
END_DATE = ""


def extract_transactions(pages: List[page.Page]) -> list:
    transactions = []

    for page in pages:
        if page.page_number < 3:
            continue

        sections = re.split(r"PURCHASE[\r\n]?|FEES CHARGED[\r\n]|[\d]{4}\s+Totals.Year.to.Date", page.extract_text(),
                            maxsplit=2 | re.IGNORECASE)
        if sections and len(sections) >= 2:
            transactions += parse_transactions(sections[1])  # Deposits
        else:
            continue

    return transactions


def parse_transactions(section: str) -> list:
    transactions = []
    matches = re.findall(
        r'(\d+\/\d+)\s+((?:(?!\d+[.,]\d+\b).)*)(?:\s*(?!\d+\/\d)(\d+(?:[.,]\d+)*)).*((?:\n(?!\d+\/\d+).*)*)', section)

    if matches:
        for match in matches:
            if match[1].strip().casefold() == "CANADIAN DOLLAR".casefold() or \
                    match[1].strip().casefold() == "COLOMBIAN PESO".casefold() or \
                    match[1].strip().casefold() == "DOMINICAN PESO".casefold():
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
            # tx_type = match[1].strip()

            # TODO: Revise tx_amount grooming
            tx_amount = "{:0.2f}".format(float(match[2].replace(',', ''))) if match[2] else None
            # Replace all types of whitespaces with a single space
            tx_description = " ".join(re.sub(r'[\s]+', ' ', match[1]).splitlines()).strip() if match[1] else None

            tags = extract_tags(tx_description)
            tx_deductible = is_deductible(tags)
            transactions.append({
                "Date": tx_date,
                "Amount": tx_amount,
                "Description": tx_description,
                "Tax Deductible": tx_deductible,
                "Category": tags
            })
    return transactions


def parse_statement_range(pdf: page.Page) -> dict:
    global START_DATE
    global END_DATE
    text = pdf.extract_text()

    date_range = re.search(r"Opening\/Closing Date (.*)", text, re.IGNORECASE).groups()[0]
    date_range = date_range.split(" - ")

    START_DATE = datetime.strptime(f"{date_range[0]}", '%m/%d/%y').strftime('%m/%d/%Y')
    END_DATE = datetime.strptime(f"{date_range[1]}", '%m/%d/%y').strftime('%m/%d/%Y')
    return {
        'start_date': START_DATE,
        'end_date': END_DATE
    }
