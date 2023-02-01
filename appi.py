import os
import requests
from flask import Flask, jsonify, request
from flask_cors import CORS, cross_origin
from jinja2 import Environment, FileSystemLoader
import pdfkit
from sendgrid import SendGridAPIClient
# from sendgrid.helpers.mail import Mail, Attachment, Email

# app = Flask(__name__)

# cors = CORS(app, resources={r"/generate-pdf": {"origins": "https://jefferson.co1.qualtrics.com"}})

@app.route('/generate-pdf', methods=['POST'])
@cross_origin(origin="https://jefferson.co1.qualtrics.com")
def generate_pdf():
    data = request.get_json()
    name = data['name']
    print("this is the name", name)
    # Render the template with the variable
    env = Environment(loader=FileSystemLoader('templates'))
    template = env.get_template('template.html')
    html = template.render(name=name)

    pdfkit.configuration(wkhtmltopdf='/usr/local/bin/wkhtmltopdf')
    # write the html to file
    with open("template.html", "w") as file:
        file.write(html)

    pdfkit.from_file("template.html", "template.pdf")

    # Send email with PDF attachment
    try:
        session = requests.Session()
        session.verify = False
        sg = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
        with open("template.pdf", "rb") as f:
            data = f.read()
        attachment = Attachment(file_content=data, file_name='template.pdf')
        to_email = Email("johnathan.raiss@gmail.com")
        from_email = Email("from@email.com")
        subject = 'This is a test email'
        content = "Please find the attachment"
        message = Mail(from_email, subject, to_email, content)
        print("pdf has been generated")
        message.add_attachment(attachment)
        print("email has been sent to the respondent")
        response = sg.send(message)

        # delete the file 
        os.remove("template.html")
        os.remove("template.pdf")

        return jsonify(response.status_code)
    except Exception as e:
        print(e)
        return jsonify(str(e))

if __name__ == '__main__':
    # app.run(debug=True)
