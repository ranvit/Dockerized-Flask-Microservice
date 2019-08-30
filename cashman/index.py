from flask import Flask, jsonify, request, current_app

from cashman.model.expense import Expense, ExpenseSchema
from cashman.model.income import Income, IncomeSchema
from cashman.model.transaction_type import TransactionType

import socket
import json
import psycopg2 as pg
import pickle
import traceback

app = Flask(__name__)

transactions = [
    Income('Salary', 5000),
    Income('Dividends', 2000),
    Income('Venmo', 800),
    Expense('pizza', 50),
    Expense('Rock Concert', 100)
]

# try:
conn = pg.connect(dbname='postgres', user='postgres', password='example', host='192.168.99.102')
cur = conn.cursor()

# THESE LINES BELOW HAVE TO BE ADDED IF THE DATABASE IS BEING INITIALIZED
# SOME COMBINATION OF "CREATE IF NOT EXISTS, AND INSERT"

    # cur.execute("ROLLBACK")
    # conn.commit()
    # cur.execute("DROP TABLE IF EXISTS byte_store;")
    # cur.execute("CREATE TABLE byte_store (trans bytea);")
    # for tr in transactions:
    #     cur.execute("INSERT INTO byte_store (trans) VALUES (%s);", (pg.Binary(pickle.dumps(tr)),))
    # conn.commit()
# except:
#     print("Initialization of Database Failed =(")

@app.route('/incomes')
def get_incomes():
    op = 0
    conn = pg.connect(dbname='postgres', user='postgres', password='example', host='192.168.99.102')
    cur = conn.cursor()

    cur.execute("SELECT * FROM byte_store")
    trs = cur.fetchall()
    trs = [pickle.loads(bytes(i[0])) for i in trs]
    schema = IncomeSchema(many=True)
    incomes = schema.dump(
        filter(lambda t: t.type == TransactionType.INCOME, trs)
    )
    
    resp = json.dumps(incomes.data, sort_keys = True, indent = 4, separators = (',', ': '))
    return current_app.response_class(resp, mimetype="application/json")

    # return jsonify(incomes.data)

    # html = "<h3>Hello world!</h3>" \
    #        "<b>Hostname Changed!:</b> {hostname}<br/>" \
    #        "<b>Incomes:</b> {visits}"
    # return html.format(hostname=socket.gethostname(), visits=resp)


@app.route('/incomes', methods=['POST'])
def add_income():
    conn = pg.connect(dbname='postgres', user='postgres', password='example', host='192.168.99.102')
    cur = conn.cursor()
    income = IncomeSchema().load(request.get_json())
    sample = pickle.dumps(income.data)
    cur.execute("INSERT INTO byte_store (trans) VALUES (%s);", (pg.Binary(sample),))
    conn.commit()
    # transactions.append(income.data)
    return '', 204


@app.route('/expenses')
def get_expenses():
    conn = pg.connect(dbname='postgres', user='postgres', password='example', host='192.168.99.102')
    cur = conn.cursor()
    cur.execute("SELECT * FROM byte_store")
    trs = cur.fetchall()
    trs = [pickle.loads(bytes(i[0])) for i in trs]

    schema = ExpenseSchema(many=True)
    expenses = schema.dump(
        filter(lambda t: t.type == TransactionType.EXPENSE, trs)
    )

    resp = json.dumps(expenses.data, sort_keys = True, indent = 4, separators = (',', ': '))
    return current_app.response_class(resp, mimetype="application/json")

    # return jsonify(expenses.data)

    # html = "<h3>Hello world!</h3>" \
    #        "<b>Hostname Changed!:</b> {hostname}<br/>" \
    #        "<b>Expenses:</b> {visits}"
    # return html.format(hostname=socket.gethostname(), visits=resp)


@app.route('/expenses', methods=['POST'])
def add_expense():
    conn = pg.connect(dbname='postgres', user='postgres', password='example', host='192.168.99.102')
    cur = conn.cursor()
    expense = ExpenseSchema().load(request.get_json())
    sample = pickle.dumps(expense.data)
    cur.execute("INSERT INTO byte_store (trans) VALUES (%s);", (pg.Binary(sample),))
    conn.commit()
    # transactions.append(expense.data)
    return '', 204


if __name__ == "__main__":
    app.run()
