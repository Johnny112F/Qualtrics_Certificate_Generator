from flask import Flask, jsonify, request, render_template, send_file
import constants
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

app = Flask(__name__)
cors = CORS(app, resources={r"/generate-pdf": {"origins": "https://jefferson.co1.qualtrics.com"}, r"/download": {"origins": "https://jefferson.co1.qualtrics.com"}})



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

    return jsonify(download_link='http://127.0.0.1:5000/download')


@app.route('/download')
@cross_origin(origin="https://jefferson.co1.qualtrics.com")
def download_pdf():
    return send_file("test.pdf", as_attachment=True)


@app.route('/upload', methods=['POST'])
@cross_origin(origin="https://jefferson.co1.qualtrics.com")
def upload_pdf():

    data = request.get_json()
    response_id = data['responseID']
    print(f'is the response id here{response_id}')

    qualtrics_key = constants.QUALTRICS_API_TOKEN
    QUALTRICS_DATA_CENTER = 'https://jefferson.co1.qualtrics.com/'
    SURVEY_ID = 'SV_cxcikvalyeZIiWO'

    url = f'https://jefferson.co1.qualtrics.com/API/v3/surveys/{SURVEY_ID}/responses/{response_id}'
    headers = {
        'content-type': 'application/json',
        'x-api-token': qualtrics_key
    }

    with open("test.pdf", 'rb') as pdf_file:
        files = {'file': pdf_file}
        response = requests.post(url, headers=headers, files=files)
    if response.status_code == 200:
        return 'File successfully uploaded'
    else:
        return f'Error uploading file. Status code: {response.status_code}. Error: {response.json()["meta"]["error"]}'


if __name__ == '__main__':
    app.run(debug=True)

