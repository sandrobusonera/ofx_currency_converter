# -*- coding: utf-8 -*-
import sys

from Cheetah.Template import Template
from ofx_parse import OfxParser


def convert_ofx_amounts(source_path, exchange_rate):
    extension = source_path.split('.')
    assert extension[-1] == "ofx", "Please provide an OFX file"

    context = _get_template_context(source_path, exchange_rate)
    rendering = Template(file="templates/ofx_currency_converter/template.ofx", searchList=[context])

    new_current = open("%s_updated.ofx" % source_path, "w")
    new_current.write(str(rendering))

def _get_template_context(ofx_file, exchange_rate):
    ofx = OfxParser.parse(file(ofx_file))

    context = dict(ofx.bank_account.__dict__)
    context['statement'] = dict(ofx.bank_account.statement.__dict__)
    context['statement']['transactions'] = []

    context['statement']['balance'] = float(context['statement']['balance']) * float(exchange_rate)

    transactions = ofx.bank_account.statement.transactions
    for transaction in transactions:
        transaction.amount = float(transaction.amount) * float(exchange_rate)
        context['statement']['transactions'].append(transaction.__dict__)

    return context

if __name__ == '__main__':
    source_path = sys.argv[1]
    exchange_rate = sys.argv[2]
    convert_ofx_amounts(source_path, exchange_rate)