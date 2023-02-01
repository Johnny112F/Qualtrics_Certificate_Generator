import os
import smtplib
import base64
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.utils import COMMASPACE, formatdate
from email import encoders
from flask import Flask, jsonify, request, render_template, send_file
from flask_cors import CORS, cross_origin
from jinja2 import Environment, FileSystemLoader
import pdfkit

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

    # Send email with PDF attachment
    try:
        msg = MIMEMultipart()
        msg['From'] = 'from@email.com'
        msg['To'] = 'johnathan.raiss@gmail.com'
        msg['Date'] = formatdate(localtime=True)
        msg['Subject'] = 'This is a test email'
        msg.attach(MIMEText("Please find the attachment"))
        
        with open("test.pdf", "rb") as f:
            part = MIMEBase('application', "octet-stream")
            part.set_payload(f.read())
            encoders.encode_base64(part)
            part.add_header('Content-Disposition', 'attachment', filename='test.pdf')
            msg.attach(part)

        smtp_server = smtplib.SMTP('::1', 1025)
        smtp_server.sendmail(msg['From'], msg['To'], msg.as_string())
        smtp_server.quit()
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
    app.run(debug=True)
