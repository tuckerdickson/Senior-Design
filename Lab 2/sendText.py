import serial
import time
from twilio.rest import Client
from datetime import datetime


# ----------------------------------------------------------------------------------------------------------------------
# Description: This function sends texts to a hard-coded number using twilio's rest library
# Inputs: None
# Output: None
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
    textStr = 'Critical Safety Event at {} on {}'.format(currTime, currDate)

    # send the message
    message = client.messages.create(
        body=textStr,
        from_=fromNum,
        to=toNum)


# ----------------------------------------------------------------------------------------------------------------------
# Description: This function waits to receive messages from the arduino. Once a message
#               is received (and enough time has elapsed) it sends a text message to the user.
# Inputs: None
# Output: None
# ----------------------------------------------------------------------------------------------------------------------
def waitForIndication():
    timeBetweenTexts = 30
    start = time.time() - timeBetweenTexts

    # open serial communication with arduino
    serialObject = serial.Serial('com4', 115200)

    # loop indefinitely
    while True:

        # evaluates to true if there is data that needs to be read in
        if serialObject.inWaiting() != 0:

            # read in the message
            value = serialObject.readline()

            # calculate the time that has elapsed since the last text was sent
            elapsedTime = time.time() - start

            # don't spam the user
            if elapsedTime >= timeBetweenTexts:
                start = time.time()
                print(value)
                sendText()

    #serialObject.close()


# ----------------------------------------------------------------------------------------------------------------------
# Description: This is the main function for sendText.py. It kicks off the program by
#               invoking waitForIndication().
# Inputs: None
# Output: None
# ----------------------------------------------------------------------------------------------------------------------

if __name__ == "__main__":
    waitForIndication()
