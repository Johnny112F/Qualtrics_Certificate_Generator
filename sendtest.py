import os
from dotenv import load_dotenv
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

load_dotenv('./sendgrid.env')
key = os.getenv('SENDGRID_API_KEY')

print("this is the API key right here " + key)

message = Mail(
    to_emails="johnathan.raiss@gmail.com",
    from_email="from@email.com",
    subject='Sending with Twilio SendGrid is Fun',
    html_content='<strong>and easy to do anywhere, even with Python</strong>')
try:
    sg = SendGridAPIClient(key)
    response = sg.send(message)
    print(response.status_code)
    print(response.body)
    print(response.headers)
except Exception as e:
    print(e)