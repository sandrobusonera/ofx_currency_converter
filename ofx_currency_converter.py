# -*- coding: utf-8 -*-
import csv
import sys

from Cheetah.Template import Template
from ofx_parse import OfxParser


def main(source_path, rate_exchange):
    extension = source_path.split('.')
    context = None
    if extension[-1] == "csv":
        context = csv_to_ofx(source_path, rate_exchange)
    elif extension[-1] == "ofx":
        context = ofx_to_ofx(source_path, rate_exchange)

    rendering = Template(file="templates/ofx_currency_converter/template.ofx", searchList=[context])

    new_current = open("%s_updated.ofx" % source_path, "w")
    new_current.write(str(rendering))

def csv_to_ofx(csv_file, rate_exchange):
    transactions = []
    with open(csv_file, 'rU') as csvfile:
        csv_read = csv.reader(csvfile, delimiter='m;')
        for line_number, row in enumerate(csv_read):
            if line_number != 0:
                transaction_date = row[0].split('/')
                name = row[1]
                amount = float(row[3].replace(',', '.'))
                amount_converted = amount * rate_exchange

                transactions.append({
                    'date': transaction_date,
                    'name': name,
                    'amount': amount_converted,
                })

    return transactions

def ofx_to_ofx(ofx_file, rate_exchange):
    ofx = OfxParser.parse(file(ofx_file))

    context = dict(ofx.bank_account.__dict__)
    context['statement'] = dict(ofx.bank_account.statement.__dict__)
    context['statement']['transactions'] = []

    context['statement']['balance'] = float(context['statement']['balance']) * float(rate_exchange)

    transactions = ofx.bank_account.statement.transactions
    for transaction in transactions:
        transaction.amount = float(transaction.amount) * float(rate_exchange)
        context['statement']['transactions'].append(transaction.__dict__)

    return context

if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2])