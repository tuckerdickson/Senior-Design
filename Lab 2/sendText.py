import serial
from twilio.rest import Client
from datetime import datetime


# ----------------------------------------------------------------------------------------------------------------------
# Description:
# Inputs:
# Output:
# ----------------------------------------------------------------------------------------------------------------------
def sendText():
    # Find your Account SID and Auth Token at twilio.com/console
    account_sid = 'ACb75f516832e3fb47abfae14aa6a45dcc'
    auth_token = '50a3900dad148b96a76d9f075c5e82fb'
    client = Client(account_sid, auth_token)

    # hard-coded sending and receiving phone number
    toNum = '+13196401169'  # '+18479177782'
    fromNum = '+19704505421'

    # get the current local date and time
    now = datetime.now()

    # format time as HH:MM XX and date as Month/Day/2022
    currTime = now.strftime('%I:%M %p')
    currDate = now.strftime('%m/%d/%Y')

    # craft the message to be sent, using currTime and currDate
    textStr = f'Critical Safety Event at {currTime} on {currDate}'

    # send the message
    message = client.messages.create(
        body=textStr,
        from_=fromNum,
        to=toNum)


# ----------------------------------------------------------------------------------------------------------------------
# Description:
# Inputs:
# Output:
# ----------------------------------------------------------------------------------------------------------------------
def waitForIndication():
    while True:
        if serialObject.inWaiting() != 0:
            value = serialObject.readline()
            print(value)
            #sendText()


if __name__ == "__main__":
    serialObject = serial.Serial('com4', 115200)
    waitForIndication()
    serialObject.close()
