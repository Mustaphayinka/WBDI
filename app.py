from flask import Flask, render_template, Response, request, send_file
import os
import pandas as pd
import matplotlib.pyplot as plt
import wbdata



# Initialize flask app
app = Flask(__name__)


# endpoints
@app.route('/', methods = ['GET', 'POST'])
def index():
    return render_template('index.html')


variables = {
             "INFLATION"  : "FP.CPI.TOTL.ZG", 
             "POPULATION" : "SP.POP.TOTL",
             "POPULATION GROWTH" : "SP.POP.GROW",
             "GDP GROWTH" : "NY.GDP.MKTP.KD.ZG",
             "GDP PER CAPITA GROWTH": "NY.GDP.PCAP.KD.ZG",
             "FOREIGN DIRECT INVESTMENT" : "BX.KLT.DINV.CD.WD",
             "REAL GDP" : "NY.GDP.MKTP.KD",
             "HUMAN DEVELOPMENT INDEX" : "UNDP.HDI.XD",
             "NORMINAL GDP" : "NY.GDP.MKTP.CD",
             "IMPORTS OF GOODS AND SERVICES" : "NE.IMP.GNFS.ZS",
             "LENDING INTEREST RATE" : "FR.INR.LEND",
             }

@app.route('/getData', methods = ['GET', 'POST'])
def getData():
    if request.method == 'POST':
        ticker = request.form['ticker']
        ticker = ticker.upper()
        # variables[ticker]
        data = wbdata.get_data(variables[ticker], country="NGA")  
        infl = dict([(int(d['date']), float(d['value'])) for d in data if d['value'] is not None])  
        # infl.values()
        infl = pd.DataFrame(infl.items(), columns=['Date', ticker])
        path = '{}.csv'.format(ticker)
        infl.to_csv(path, index = None)
        # path = '{}.csv'.format(ticker)
        return send_file(path, as_attachment=True)
    return render_template('index.html')

if __name__ == "__main__":
    app.run(debug = True)
