from flask import Flask
from flask import render_template, request
import requests
import csv

app = Flask(__name__)

# 1 get information from the bank
response = requests.get(
    "http://api.nbp.pl/api/exchangerates/tables/C?format=json")
data = response.json()

# 2 def 'data' list (with 'currency', 'code', 'bid', 'ask')
rates = data[0]['rates']
code_ex = [rates[i]['code'] for i, j in enumerate(rates)]
actual_date = data[0]['effectiveDate']


def export_data_to_csv():
    with open('details{}.csv'.format(actual_date), 'w', newline='') as csvfile:
        details = csv.writer(csvfile, delimiter=';')
        details.writerow(['currency', 'code', 'bid', 'ask'])
        for i, j in enumerate(rates):
            cur = rates[i]['currency']
            cod = rates[i]['code']
            bid = rates[i]['bid']
            ask = rates[i]['ask']
            details.writerow([cur, cod, bid, ask])


@app.route("/", methods=['GET', 'POST'])
def main():
    if request.method == 'GET':
        return render_template("form.html", code_ex=code_ex)
    elif request.method == 'POST':
        code = request.form.get("code")
        amount = float(request.form.get("amount"))
        for i, j in enumerate(rates):
            if code == rates[i]['code']:
                currency = rates[i]['currency']
                ask = float(rates[i]['ask'])
        result = amount * ask
        return render_template(
            'result.html', code=code, amount=amount,
            currency=currency, ask=ask, result=result)


# 5 run program
if __name__ == "__main__":
    export_data_to_csv()
    app.run()
