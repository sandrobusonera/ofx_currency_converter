# -*- coding: utf-8 -*-
import sys

from Cheetah.Template import Template
from ofxparse import OfxParser


def convert_ofx_amounts(source_path, exchange_rate):
    extension = source_path.split('.')
    assert extension[-1] == "ofx", "Please provide an OFX file"

    context = _get_template_context(source_path, exchange_rate)
    rendering = Template(file="templates/template.ofx", searchList=[context])

    new_current = open("%s_updated.ofx" % source_path, "w")
    new_current.write(str(rendering))

def _get_template_context(ofx_file, exchange_rate):
    ofx = OfxParser.parse(file(ofx_file))

    context = dict(ofx.account.__dict__)
    context['statement'] = dict(context['statement'].__dict__)
    context['statement']['balance'] = _convert_amount(context['statement']['balance'], exchange_rate)
    context['statement']['start_date'] = _date_to_text(context['statement']['start_date'])
    context['statement']['end_date'] = _date_to_text(context['statement']['end_date'])

    transactions = context['statement']['transactions']
    context['statement']['transactions'] = _convert_amount_transactions(transactions, exchange_rate)

    return context

def _convert_amount(amount, exchange_rate):
    return float(amount) * float(exchange_rate)

def _date_to_text(date):
    return "%s%s%s000000[-5:EST]" % (date.year, date.month, date.day)

def _convert_amount_transactions(transactions, exchange_rate):
    transactions_converted = []
    for transaction in transactions:
        transaction.amount = _convert_amount(transaction.amount, exchange_rate)
        transaction.date = _date_to_text(transaction.date)
        transactions_converted.append(transaction.__dict__)

    return transactions_converted

if __name__ == '__main__':
    source_path = sys.argv[1]
    exchange_rate = sys.argv[2]
    convert_ofx_amounts(source_path, exchange_rate)