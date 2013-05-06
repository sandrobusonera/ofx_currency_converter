# -*- coding: utf-8 -*-
import sys

from Cheetah.Template import Template
from ofxparse import OfxParser

#TK
import tkMessageBox
import Tkinter,tkFileDialog

def pick_file(title):
    root = Tkinter.Tk()
    return tkFileDialog.askopenfilename(parent=root,title=title)

def convert_ofx_amounts(source_path, exchange_rate):
    extension = source_path.split('.')
    assert extension[-1] == "ofx", "Please provide an OFX file"

    context = _get_template_context(source_path, exchange_rate)
    rendering = Template(open(_resource_path("templates/template.ofx")).read(), searchList=[context])

    new_current = open("%s_updated.ofx" % source_path, "w")
    new_current.write(str(rendering))

def _resource_path(relative):
    return os.path.join(
        os.environ.get(
            "_MEIPASS2",
            os.path.abspath(".")
        ),
        relative
    )

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
    ofx_file = pick_file('Choose the private key corresponding on the project you would like to decrypt')
    currency_exchange_rate = "1.175"
    convert_ofx_amounts(ofx_file, currency_exchange_rate)
