import random
import json
from time import time
import random
from flask import Flask, render_template, url_for, request, redirect, make_response

app = Flask(__name__)
start = time()


@app.route('/', methods=['GET', 'POST'])
def home():
    return render_template('chart.html')


@app.route('/data', methods=['GET', 'POST'])
def data():
    stop = time()
    t = stop - start
    temp = random.randint(70, 80)
    data = [t, temp]

    response = make_response(json.dumps(data))
    response.content_type = 'application/json'

    return response


if __name__ == '__main__':
    app.run(debug=True)
