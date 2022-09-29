import serial
import json
from flask import Flask, render_template, request, make_response
from twilio.rest import Client

app = Flask(__name__)
fahrenheit = open('fahrenheit.txt', 'w')
celsius = open('celsius.txt', 'w')

# ----------------------------------------------------------------------------------------------------------------------
# Description: This function sends a text to the specified phone number when the temperature falls outside the bound.
# Inputs: The temperature bounds (lowtemp and hightemp), the corresponding messages, the phone number to send to, and
#           the current temperature.
# Output: None
# ----------------------------------------------------------------------------------------------------------------------
def sendText(lowtemp, hightemp, lowmessage, highmessage, phonenum, temperature):
    # Find your Account SID and Auth Token at twilio.com/console
    account_sid = 'ACb75f516832e3fb47abfae14aa6a45dcc'
    auth_token = '50a3900dad148b96a76d9f075c5e82fb'
    client = Client(account_sid, auth_token)

    # send a text if temperature is higher than hightemp
    if temperature > hightemp:
        message = client.messages.create(
            body=highmessage,
            from_='+19704505421',
            to=phonenum)

    # send a text if temperature is lower than lowtemp
    elif temperature < lowtemp:
        message = client.messages.create(
            body=lowmessage,
            from_='+19704505421',
            to=phonenum)


# ----------------------------------------------------------------------------------------------------------------------
# Description: This function receives a temperature reading from the arduino via serial communication.
# Inputs: None
# Output: The temperature read in (as a float)
# ----------------------------------------------------------------------------------------------------------------------
def getTemperature():
    # start up a serial communication on the port shared by the arduino
    serialObject = serial.Serial('com4', 9600)

    # loop while there are zero bytes waiting to be read (in other words, wait until there are bytes to be read)
    while serialObject.inWaiting() == 0:
        pass

    # read in the temperature
    temperature = serialObject.readline()

    # close the serial channel
    serialObject.close()

    # return the temperature as a float
    return float(temperature)


# ----------------------------------------------------------------------------------------------------------------------
# Description: This function was intended to send a flag to the arduino when the "virtual button" on the website was
#               pressed. We were not able to get two-way serial communication to work
# Inputs: A string to be sent to the arduino.
# Output: None
# ----------------------------------------------------------------------------------------------------------------------
# def sendButtonFlag(flag):
#     serialObject = serial.Serial('com4', 9600, timeout=0.1)
#
#     while serialObject.inWaiting() > 0:
#         pass
#
#     serialObject.write(bytes(flag))
#     serialObject.close()
#
#     return


# ----------------------------------------------------------------------------------------------------------------------
# Description: This function is called when the website is routed to the home ('/') page. It contains a 'POST' method,
#               which reads information from the chart.html and passes it along to sendText().
# Inputs: None
# Output: The rendered chart.html template.
# ----------------------------------------------------------------------------------------------------------------------
@app.route('/', methods=['GET', 'POST'])
def home():
    # POST method handles gathering temperature information and passing it to sendText()
    if request.method == 'POST':
        # gather temperature information from chart.html
        lowTemp = request.form['lowTemp']
        highTemp = request.form['highTemp']
        lowMessage = request.form['lowMessage']
        highMessage = request.form['highMessage']
        phone = request.form['phone']
        temperature = request.form['temperature']

        # pass the gathered information to sendText() to send an SMS message
        sendText(lowTemp, highTemp, lowMessage, highMessage, phone, temperature)

    # return the rendered chart.html template
    return render_template('chart.html')


# ----------------------------------------------------------------------------------------------------------------------
# Description: This function is called when the website is routed to the /data page. It contains a 'GET' method,
#               which gets a temperature reading from getTemperature() and passes it to chart.html to be displayed on
#               the website. We also attempted to include a POST method, which would handle the virtual button, but
#               weren't successful.
# Inputs: None
# Output: The response message to the json temperature dump.
# ----------------------------------------------------------------------------------------------------------------------
@app.route('/data', methods=['GET', 'POST'])
def data():
    # handles GET request from html file
    if request.method == 'GET':
        # call test() to get temperature data
        temp = getTemperature()

        # craft a json-formatted response containing the time and temp reading
        response = make_response(json.dumps([0, temp]))
        response.content_type = 'application/json'

        # return response
        return response

    # if request.method == 'POST':
    #     virtualButtonPressed = request.form['buttonPressed']
    #     print(virtualButtonPressed)
    #     sendButtonFlag(virtualButtonPressed)
    #     return


# ----------------------------------------------------------------------------------------------------------------------
# Description: This is the main function, which is called when the project is run. It kicks off the chain of events
#               which starts the web server.
# Inputs: None
# Output: None
# ----------------------------------------------------------------------------------------------------------------------
if __name__ == '__main__':
    app.run(debug=True)
