# Download the helper library from https://www.twilio.com/docs/python/install
from twilio.rest import Client

# Find your Account SID and Auth Token at twilio.com/console
account_sid = 'ACb75f516832e3fb47abfae14aa6a45dcc'
auth_token = '50a3900dad148b96a76d9f075c5e82fb'
client = Client(account_sid, auth_token)

#dummy, won't be in actual code in this form
#comes from temp sensor data
temperature = 20
#comes from user input on webpage
hightemp = 25
lowtemp = 15
highmessage = 'Temperature is above 25 C'
lowmessage = 'Temperature is below 15 C'
phonenum = '+18479177782'


#send a text if temperature is higher than 25 C
if (temperature > hightemp):
    message = client.messages.create(
            body = highmessage,
            from_ = '+19704505421',
            to = phonenum)
#send a text if temperature is lower than 15 C
elif (temperature < lowtemp):
    message = client.messages.create(
            body = lowmessage,
            from_ = '+19704505421',
            to = phonenum)