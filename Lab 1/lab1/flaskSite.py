import random
import json
from time import time
import random
from flask import Flask, render_template, url_for, request, redirect, make_response
from twilio.rest import Client

app = Flask(__name__)
start = time()


def sendText(lowtemp, hightemp, lowmessage, highmessage, phonenum, temperature):
    # Find your Account SID and Auth Token at twilio.com/console
    account_sid = 'ACb75f516832e3fb47abfae14aa6a45dcc'
    auth_token = '50a3900dad148b96a76d9f075c5e82fb'
    client = Client(account_sid, auth_token)

    # send a text if temperature is higher than 25 C
    if temperature > hightemp:
        message = client.messages.create(
            body=highmessage,
            from_='+19704505421',
            to=phonenum)
    # send a text if temperature is lower than 15 C
    elif temperature < lowtemp:
        message = client.messages.create(
            body=lowmessage,
            from_='+19704505421',
            to=phonenum)


@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        lowTemp = request.form['lowTemp']
        highTemp = request.form['highTemp']
        lowMessage = request.form['lowMessage']
        highMessage = request.form['highMessage']
        phone = request.form['phone']
        temperature = request.form['temperature']

        print("lowTemp: ", lowTemp)
        print("highTemp: ", highTemp)
        print("lowMessage: ", lowMessage)
        print("highMessage: ", highMessage)
        print("phone: ", phone)
        print("temperature: ", temperature)

        sendText(lowTemp, highTemp, lowMessage, highMessage, phone, temperature)

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
