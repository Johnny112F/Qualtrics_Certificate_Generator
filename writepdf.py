from flask import Flask, jsonify, request, render_template, send_file
import os
import requests
import pdfrw
from flask_cors import CORS, cross_origin
from jinja2 import Environment, FileSystemLoader
from PyPDF2 import PdfReader, PdfWriter
import pdfkit
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail, Attachment, Email
from pathlib import Path
import pdfrw


app = Flask(__name__)
cors = CORS(app, resources={r"/generate-pdf": {"origins": "https://jefferson.co1.qualtrics.com"}})


@app.route('/generate-pdf', methods=['POST'])
@cross_origin(origin="https://jefferson.co1.qualtrics.com")
def generate_pdf():
    print(os.getcwd())
    data = request.get_json()
    name = data['name']

    # pdf_path = (
    #      Path.home()
    #      "certjr.pdf"
    #  )
    # pdf_path = os.path.join(os.getcwd(), '/Users/johnathanraiss/qualtrics_server/certjr.pdf')
    # pdf = pdfrw.PdfReader(pdf_path)
    # Open the certificate PDF
    files = os.listdir('/Users/johnathanraiss/qualtrics_server')

    os.chdir('/Users/johnathanraiss/qualtrics_server')
    pdfs = []
    for file in glob.glob("*.pdf"):
        print(file)
        pdfs.append(file)
    # pdf = pdfrw.PdfReader(pdf_path)
    if(pdf_path):
        print("ITS HERE NOW")
    else:
        print("NOT HERE ALERT")
    # Replace the text in the pdf
    for page in pdf.pages:
        for key, field in page.items():
            if field.get('/T') == "Johnathan Raiss":
                field.update(pdfrw.PdfDict(V=name))
        # Save the changes to the PDF
        pdfrw.PdfWriter().write("certjrr.pdf", pdf)
        # get the current working directory
        current_directory = os.getcwd()

        # specify the directory path where the pdf will be saved
        pdf_directory = os.path.join(current_directory, 'pdfs')

        # create the full path to the pdf file
        pdf_path = os.path.join(pdf_directory, 'certjrr.pdf')

        # use pdfrw to save the pdf to the specified directory
    pdfrw.PdfWriter().write(pdf_path, pdf)
    # Send email with PDF attachment
    try:
        session = requests.Session()
        session.verify = False
        sg = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
        with open("certjrr.pdf", "rb") as f:
            data = f.read()
        attachment = Attachment(file_content=data, file_name='certjrr.pdf')
        to_email = Email("johnathan.raiss@gmail.com")
        from_email = Email("from@email.com")
        subject = 'This is a test email'
        content = "Please find the attachment"
        message = Mail(from_email, subject, to_email, content)
        message.add_attachment(attachment)
        response = sg.send(message)
        print(response.status_code)
        print(response.body)
        print(response.headers)
    except Exception as e:
        # print(e)
        return jsonify(str(e))

    # return the pdf to the user with a link to download 
    return render_template('certjrr.html')


@app.route('/download')
@cross_origin(origin="https://jefferson.co1.qualtrics.com")
def download_pdf():
    return send_file("certjrr.pdf", as_attachment=True)


if __name__ == '__main__':
    app.run(debug=True)
