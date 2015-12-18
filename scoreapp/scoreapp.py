from datetime import datetime
import re
import json

import requests
from bs4 import BeautifulSoup
import pandas as pd

from flask import (
    Flask,
    abort,
    flash,
    redirect,
    render_template,
    request,
    url_for
)

from scorer import weighted_scores

app = Flask(__name__)
app.config['DEBUG'] = True

def _fetch_code(longcode):
    print longcode
    codematch = re.compile('(?<=nep-)[a-z]{3}$')
    match = codematch.search(longcode)
    if not match:
        return False
    start, end = match.span()
    return longcode[start:end]

@app.route('/')
def show_home():

    codetable = pd.read_html('http://nep.repec.org/')[1]
    codes = pd.DataFrame(codetable.loc[1:])
    codes.columns = codetable.loc[0]
    codes['access'] = codes['access'].str[4:]
    codes = [
        {'code': row['access'],
         'long': row['title']} for _, row in codes.iterrows()
    ]
    fold = len(codes) // 2 + 1
    return render_template('landing.html', codes=codes)

@app.route('/process', methods=['POST'])
def process_form():
    formData = request.values
    codes = [(code, weight) for code, weight in formData.items()
             if float(weight) > 0]
    codes3 = map(lambda x: x[0][:3], codes)
    weights = map(lambda x: float(x[1]), codes)
    pd.set_option('max_colwidth', 100)
    table = weighted_scores(codes3, weights).reset_index().to_html(index=False)
    return render_template('results.html', table=table, codes=', '.join(codes3))

if __name__ == '__main__':
    app.run()
