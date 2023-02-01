from flask import Flask, jsonify, request, render_template, send_file
import os
import requests
import base64
from email.utils import COMMASPACE, formatdate
from email import encoders
from flask_cors import CORS, cross_origin
from jinja2 import Environment, FileSystemLoader
import pdfkit
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail, Attachment, Email

# app = Flask(__name__)
# cors = CORS(app, resources={r"/generate-pdf": {"origins": "https://jefferson.co1.qualtrics.com"}})

@app.route('/generate-pdf', methods=['POST'])
@cross_origin(origin="https://jefferson.co1.qualtrics.com")
def generate_pdf():
    data = request.get_json()
    name = data['name']

    # Render the template with the variable
    env = Environment(loader=FileSystemLoader('templates'))
    template = env.get_template('test.html')
    image_path = '/Users/johnathanraiss/qualtrics_server/page_001.jpeg'
    
    def get_base64_encoded_image(image_path):
        with open(image_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode('utf-8')

    html = template.render(name=name, image=get_base64_encoded_image(image_path))

    pdfkit.configuration(wkhtmltopdf='/usr/local/bin/wkhtmltopdf')
    # write the html to file
    with open("test.html", "w") as file:
        file.write(html)

    pdfkit.from_file("test.html", "test.pdf")

    try:
        session = requests.Session()
        session.verify = False
        sg = SendGridAPIClient(os.environ.get(''))
        with open("test.pdf", "rb") as f:
            data = f.read()
        attachment = Attachment(file_content=data, file_name='test.pdf')
        to_email = Email("johnathan.raiss@gmail.com")
        from_email = Email("from@email.com")
        subject = 'This is a test email'
        content = "Please find the attachment"
        message = Mail(from_email, subject, to_email, content)
        message.add_attachment(attachment)
        response = sg.send(message)
        # delete the file 
        # os.remove("template.html")
    except Exception as e:
        print(e)
        return jsonify(str(e))
    
    # return the pdf to the user with a link to download 
    return render_template('pdf.html')

@app.route('/download')
@cross_origin(origin="https://jefferson.co1.qualtrics.com")
def download_pdf():
    return send_file("test.pdf", as_attachment=True)

if __name__ == '__main__':
    # app.run(debug=True)
