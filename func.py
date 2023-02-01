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
    image_path = '/Users/johnathanraiss/qualtrics_server/page_001.jpeg'
    pdf_path = "test.pdf"
    pdf_name = "test.pdf"
    email_to = "johnathan.raiss@gmail.com"
    email_from = "from@email.com"
    email_subject = 'This is a test email'
    email_content = "Please find the attachment"
    render_template_and_save_to_file("test.html", name, image_path)
    generate_pdf_from_html_file("test.html", pdf_path)
    send_email_with_pdf_attachment(pdf_path, pdf_name, email_to, email_from, email_subject, email_content)
    # return render_template('test.html')

def render_template_and_save_to_file(template_name, name, image_path):
    env = Environment(loader=FileSystemLoader('templates'))
    template = env.get_template(template_name)
    def get_base64_encoded_image(image_path):
        with open(image_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode('utf-8')
    html = template.render(name=name, image=get_base64_encoded_image(image_path))
    with open(template_name, "w") as file:
        file.write(html)

def generate_pdf_from_html_file(html_file_path, pdf_file_path):
    pdfkit.configuration(wkhtmltopdf='/usr/local/bin/wkhtmltopdf')
    pdfkit.from_file(html_file_path, pdf_file_path)

def send_email_with_pdf_attachment(pdf_path, pdf_name, email_to, email_from, email_subject, email_content):
    try:
        session = requests.Session()
        session.verify = False
        sg = SendGridAPIClient(os.environ.get(''))
        with open(pdf_path, "rb") as f:
            data = f.read()
        attachment = Attachment(file_content=data, file_name=pdf_name)
        to_email = Email(email_to)
        from_email = Email(email_from)
        subject = email_subject
        content = email_content
        message = Mail(from_email, subject, to_email, content)
        message.add_attachment(attachment)
        response = sg.send(message)
        # delete the file 
        # os.remove("template.html")
    except Exception as e:
        print(e)
        return jsonify(str(e))

@app.route('/download')
@cross_origin(origin="https://jefferson.co1.qualtrics.com")
def download_pdf():
    return send_file("test.pdf", as_attachment=True)

if __name__ == '__main__':
    # app.run(debug=True)

