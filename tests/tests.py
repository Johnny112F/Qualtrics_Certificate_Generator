import unittest
from flask import Flask, jsonify, request
from flask_cors import CORS, cross_origin
from jinja2 import Environment, FileSystemLoader
from app import app, generate_pdf, download_pdf

class TestGeneratePDF(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True
    
    def test_generate_pdf(self):
        # send a POST request to the /generate-pdf endpoint
        response = self.app.post('/generate-pdf', json={'name': 'John Doe'})
        # check that the response has a status code of 200
        self.assertEqual(response.status_code, 200)
        # check that the response is a JSON object containing a link to the /download endpoint
        self.assertEqual(response.get_json(), {'download_link': 'http://127.0.0.1:5000/download'})

    def test_download_pdf(self):
        # send a GET request to the /download endpoint
        response = self.app.get('/download')
        # check that the response has a status code of 200
        self.assertEqual(response.status_code, 200)
        # check that the response is a PDF file
        self.assertEqual(response.content_type, 'application/pdf')

if __name__ == '__main__':
    unittest.main()

# import os
# import unittest
# from app import app
# from unittest.mock import patch, mock_open


# class TestPDFGeneration(unittest.TestCase):
#     def setUp(self):
#         self.app = app.test_client()

#     @patch('app.get_base64_encoded_image')
#     def test_render_template(self, mock_get_base64_encoded_image):
#         name = 'John Doe'
#         expected_output = '<html>...<h1>Certificate for John Doe</h1>...</html>'
#         mock_get_base64_encoded_image.return_value = 'encoded_image'
#         result = app.render_template(name)
#         self.assertEqual(result, expected_output)
#         mock_get_base64_encoded_image.assert_called_once_with('/Users/johnathanraiss/qualtrics_server/page_001.jpeg')

#     @patch('pdfkit.from_file')
#     def test_create_pdf(self, mock_pdfkit):
#         html = '<html>...</html>'
#         app.create_pdf(html)
#         mock_pdfkit.assert_called_once_with("test.html", "test.pdf")

#     @patch('app.SendGridAPIClient.send')
#     def test_send_email(self, mock_send):
#         pdf_path = 'test.pdf'
#         app.send_email(pdf_path)
#         mock_send.assert_called_once()

#     @patch('app.render_template')
#     @patch('app.create_pdf')
#     @patch('app.send_email')
#     def test_generate_pdf_endpoint(self, mock_render, mock_create, mock_send):
#         data = {'name': 'John Doe'}
#         response = self.app.post('/generate-pdf', json=data)
#         mock_render.assert_called_once()
#         mock_create.assert_called_once()
#         mock_send.assert_called_once()
#         self.assertEqual(response.status_code, 200)


# if __name__ == '__main__':
#     unittest.main()

