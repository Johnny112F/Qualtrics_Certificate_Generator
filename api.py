import os
import requests
from flask import Flask, jsonify, request
from flask_cors import CORS, cross_origin
from jinja2 import Environment, FileSystemLoader
import pdfkit
import json 
import base64
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail, Attachment

# app = Flask(__name__)

# cors = CORS(app, resources={r"/generate-pdf": {"origins": "https://jefferson.co1.qualtrics.com"}})

@app.route('/generate-pdf', methods=['POST'])
@cross_origin(origin="https://jefferson.co1.qualtrics.com")
def generate_pdf():
    data = request.get_json()
    name = data['name']

    # Render the template with the variable
    env = Environment(loader=FileSystemLoader('templates'))
    template = env.get_template('template.html')
    html = template.render(name=name)

    pdfkit.configuration(wkhtmltopdf='/usr/local/bin/wkhtmltopdf')
    # write the html to file
    with open("template.html", "w") as file:
        file.write(html)

    pdfkit.from_file("template.html", "template.pdf")

    # delete the file 
    # os.remove("template.html")

    # Send email with PDF attachment
    try:
        session = requests.Session()
        session.verify = False
        sg = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
        with open("template.pdf", "rb") as f:
            data = f.read()
            f.close()
        # attachment = Attachment(file_content=data, file_name='template.pdf')
        # message = Mail(
        #     from_email='from_email@example.com',
        #     to_emails='johnathan.raiss@gmail.com',
        #     subject='Certificate',
        #     html_content='<p>Please find the attachment</p>')
        # message.add_attachment(attachment)
        # json_str = json.dumps({'message': message.decode('utf-8')})
        # message_to = base64.b64encode(message.read())
        # message_data = message.decode()

        # response = sg.send(message)
        to_email = mail.Email( "johnathan.raiss@gmail.com")
        from_email = mail.Email( "from@email.com" )
        subject = 'This is a test email'
        content = mail.Content('text/plain', 'Example message.')
        message = mail.Mail(from_email, subject, to_email, content)
        response = sg.client.mail.send.post(request_body = message.get())
        return response


        print(message)
    
        print(response.status_code)
        print(response.body)
        print(response.headers)
    except Exception as e:
        print(e.message)

    return jsonify(response)

if __name__ == '__main__':
    # app.run(debug=True)