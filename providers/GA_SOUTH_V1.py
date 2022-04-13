import re

from pdfplumber import page
from typing import List
from datetime import datetime
from collections import OrderedDict

START_DATE = ""
END_DATE = ""


def extract_transactions(pages: List[page.Page]) -> dict:
    pdf = pages[0]
    text = pdf.extract_text()
    table = pdf.extract_tables()[3][1][0]
    match_date = re.search(r"Bill Date: (\d{2})\/(\d{2})\/(\d{2})", text).groups()
    bill_date = datetime.strptime(f"{match_date[0]}/{match_date[1]}/{match_date[2]}", '%m/%d/%y').strftime('%m/%d/%Y')
    bill_plan = re.search(r"Plan: (.+)", text, re.IGNORECASE).group(1)
    bill_other = re.findall(r"([\w()]+)\s[.]{5,}[$]([.\d]+)", text, re.IGNORECASE)
    bill_total = pdf.extract_tables()[1][1][2][1:]
    table_data = re.search(
        r"\s(\d{2})\s(\d+)\s(\d+)[\s=]+(\d+)[\s X]+([\d.]+)[\s=]+([\d.]+)[\s X]+([\d.]+)[\s=]+([\d.]+)",
        table,
        re.IGNORECASE)
    data = {
        "date": bill_date,
        "plan": bill_plan,
        "other": bill_other,
        "data": table_data,
        "total": bill_total
    }
    return parse_transactions(data)


def parse_transactions(data: dict) -> list:
    if not data:
        raise ValueError('oops!')
    transactions = OrderedDict({
        "Statement Date": data["date"],
        "Start Date": START_DATE,
        "End Date": END_DATE,
        "Plan": data["plan"],
        "Days of service": data["data"][1],
        "Beginning Read": data["data"][2],
        "Ending Read": data["data"][3],
        "CCFs Used": data["data"][4],
        "Therm Factor": "{:0.2f}".format(float(data["data"][5])),
        "Therms Used": "{:0.2f}".format(float(data["data"][6])),
        "Rate Per Therm": "{:0.2f}".format(float(data["data"][7])),
        "Gas Charges": "{:0.2f}".format(float(data["data"][8])),
    })
    for charge in data["other"]:
        if charge[0][:3] == "AGL":
            transactions["AGLPassThrough"] = "{:0.2f}".format(float(charge[1]))
        else:
            transactions[charge[0]] = "{:0.2f}".format(float(charge[1]))
    transactions["Total"] = "{:0.2f}".format(float(data["total"]))
    transactions.move_to_end("Total", last=True)
    return [transactions]


def parse_statement_range(pdf: page.Page) -> dict:
    global START_DATE
    global END_DATE
    text = pdf.extract_tables()[3][1]
    date_range = re.findall(r"(\d{2})\/(\d{2})\/(\d{4})", text[0])
    START_DATE = datetime.strptime(f"{date_range[0][0]}/{date_range[0][1]}/{date_range[0][2]}", '%m/%d/%Y').strftime(
        '%m/%d/%Y')
    END_DATE = datetime.strptime(f"{date_range[1][0]}/{date_range[1][1]}/{date_range[1][2]}", '%m/%d/%Y').strftime(
        '%m/%d/%Y')
    return {
        'start_date': START_DATE,
        'end_date': END_DATE
    }
