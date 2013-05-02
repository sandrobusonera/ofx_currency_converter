# -*- coding: utf-8 -*-
import sys

from Cheetah.Template import Template
from ofx_parse import OfxParser


def main(source_path, rate_exchange):
    extension = source_path.split('.')
    assert extension[-1] == "ofx", "Please provide an OFX file"

    context = ofx_to_ofx(source_path, rate_exchange)
    rendering = Template(file="templates/ofx_currency_converter/template.ofx", searchList=[context])

    new_current = open("%s_updated.ofx" % source_path, "w")
    new_current.write(str(rendering))

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