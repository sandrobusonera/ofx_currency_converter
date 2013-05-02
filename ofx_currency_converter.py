# -*- coding: utf-8 -*-
import sys

from Cheetah.Template import Template
from ofx_parse import OfxParser


def convert_ofx_amounts(source_path, exchange_rate):
    extension = source_path.split('.')
    assert extension[-1] == "ofx", "Please provide an OFX file"

    context = _get_template_context(source_path, exchange_rate)
    rendering = Template(file="templates/template.ofx", searchList=[context])

    new_current = open("%s_updated.ofx" % source_path, "w")
    new_current.write(str(rendering))

def _get_template_context(ofx_file, exchange_rate):
    ofx = OfxParser.parse(file(ofx_file))

    context = dict(ofx.bank_account.__dict__)
    context['statement'] = dict(ofx.bank_account.statement.__dict__)
    context['statement']['balance'] = _convert_amount(context['statement']['balance'], exchange_rate)

    transactions = ofx.bank_account.statement.transactions
    context['statement']['transactions'] = _convert_amount_transactions(transactions, exchange_rate)

    return context

def _convert_amount(amount, exchange_rate):
    return float(amount) * float(exchange_rate)

def _convert_amount_transactions(transactions, exchange_rate):
    transactions_converted = []
    for transaction in transactions:
        transaction.amount = _convert_amount(transaction.amount, exchange_rate)
        transactions_converted.append(transaction.__dict__)

    return transactions_converted

if __name__ == '__main__':
    source_path = sys.argv[1]
    exchange_rate = sys.argv[2]
    convert_ofx_amounts(source_path, exchange_rate)