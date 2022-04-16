import re

from pdfplumber import page
from typing import List
from datetime import datetime
from collections import OrderedDict

START_DATE = ""
END_DATE = ""


def extract_transactions(pages: List[page.Page]) -> dict:
    pdf = pages[0]
    table_settings = {
        "vertical_strategy": "text",
        "horizontal_strategy": "lines"
    }
    table = pdf.extract_table()
    # Clean up extract_table()
    table[0][6] = re.sub(r"END|READ|\n", "", table[0][6]).strip()
    table[0].append("END READ")
    fixed = table[1][6].split(" ")
    del table[1][6]
    table[1] += fixed

    text = pdf.extract_text()
    keys = list(map(lambda item: item.replace("\n", " ").title(), table[0]))
    values = list(map(lambda item: item.replace("\n", " ").title(), table[1]))
    data = OrderedDict(dict(zip(keys, values)))

    match_date = re.search(r"BILLING DATE: (\d+)\/(\d+)\/(\d+)", text).groups()
    bill_date = datetime.strptime(f"{match_date[0]}/{match_date[1]}/{match_date[2]}", '%m/%d/%Y').strftime('%m/%d/%Y')
    text = re.split("SUMMARY OF CURRENT CHARGES|New Charges Due", text)
    total_charges = re.search(r"NEW CHARGES: \$(\S+)", text[0]).groups()[0]
    current_charges = re.findall(r"([a-zA-Z]+[\w ]+).*\$([\d.]+)", text[1])
    current_charges = dict((key.strip(), value.strip()) for key, value in current_charges)

    data["Total"] = total_charges
    data["Date"] = bill_date
    data.move_to_end("Date", last=False)
    data.update(current_charges)

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
    table = pdf.extract_table()
    date_range = table[1][3].split(" — ")
    START_DATE = datetime.strptime(f"{date_range[0]}", '%m/%d/%Y').strftime(
        '%m/%d/%Y')
    END_DATE = datetime.strptime(f"{date_range[1]}", '%m/%d/%Y').strftime(
        '%m/%d/%Y')

    return {
        'start_date': START_DATE,
        'end_date': END_DATE
    }
