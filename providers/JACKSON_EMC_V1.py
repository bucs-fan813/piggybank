import re

from pdfplumber import page
from typing import List
from datetime import datetime

START_DATE = ""
END_DATE = ""


def extract_transactions(pages: List[page.Page]) -> dict:
    pdf = pages[0]
    text = pdf.extract_text()

    match_date = re.search(r"Bill Date: (\d{2})\/(\d{2})\/(\d{4})", text).groups()
    bill_date = datetime.strptime(f"{match_date[0]}/{match_date[1]}/{match_date[2]}", '%m/%d/%Y').strftime('%m/%d/%Y')
    bill_plan = re.search(r"Days of Service: (\d+)", text, re.IGNORECASE).groups()[0]
    bill_other = re.findall(r"\d{2}\/\d{2}\/\d{2}([\D ]+)\s[$](\d+\.\d+)", text, re.IGNORECASE)

    pdf = pages[1]
    text = pdf.extract_text()
    table_data = re.findall(
        r"([a-zA-Z]+)\s([\w]+)\s([\d.]+)[\r\n]",
        text,
        re.IGNORECASE)
    data = {
        "Bill Date": bill_date,
        "Days of Service": bill_plan,
        "Previous Reading": table_data[0][2],
        "Present Reading": table_data[1][2],
        "Meter Multiplier": table_data[2][2]
    }
    for transaction in bill_other:
        data[transaction[0].title()] = transaction[1]

    return [data]


def parse_transactions(data: list) -> list:
    if not data:
        raise ValueError('oops!')
    transactions = []
    for transaction in data:
        print(transaction)
        transactions += {
            "Previous Reading": transaction[0],
            "Present Reading": transaction[1],
            "Meter Multiplier": transaction[2]
        }
    return transactions


def parse_statement_range(pdf: page.Page) -> dict:
    global START_DATE
    global END_DATE
    text = pdf.extract_text()
    date_range = re.search(r"Service period: (\w+)\s(\d+)[, ]+(\d+)[\s\W]+(\w+)\s(\d+)[, ]+(\d+)", text)
    START_DATE = datetime.strptime(f"{date_range[1]} {date_range[2]}, {date_range[3]}", '%b %d, %Y').strftime(
        '%m/%d/%Y')
    END_DATE = datetime.strptime(f"{date_range[4]} {date_range[5]}, {date_range[6]}", '%b %d, %Y').strftime(
        '%m/%d/%Y')

    return {
        'start_date': START_DATE,
        'end_date': END_DATE
    }
