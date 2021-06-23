from flask import Flask, jsonify, request
from flask_restful import Resource, Api
from pdf2image import convert_from_path,convert_from_bytes
from base64 import b64decode
import base64
import json

app = Flask(__name__)
api = Api(app)

class ConvertPdfToImage(Resource):

    #Irá receber um pdf em base 64 -> converter para pdf -> converter o pdf para imagem -> converter a imagem para base64 -> enviar base64 ba resposta
    def post(self):
        dados = json.loads(request.data)
        pdf_base64 = str(dados['pdf_string'])

        #Conversão base64 para pdf
        bytes = b64decode(pdf_base64, validate=True)
        if bytes[0:4] != b'%PDF':
            raise ValueError('Missing the PDF file signature')

        file = open('newPdf.pdf', 'wb')
        file.write(bytes)
        file.close

        pages = convert_from_path('newPdf.pdf', 500)
        for page in pages:
            page.save('ImageConverted.jpg', 'JPEG')

        with open("ImageConverted.jpg", "rb") as img_file:
            imageBase64 = base64.b64encode(img_file.read())

        strImgeBase64 = str(imageBase64)
        #print(strImgeBase64[2:-1])
      
        return {'Return': strImgeBase64[2:-1]}

api.add_resource(ConvertPdfToImage, '/convert')

#file = open('new.pdf', 'wb')
#for line in open('code.txt', 'rb').readlines():
#    file.write(line)
#file.close()

#pages = convert_from_path('new.pdf', 500)
#pages = convert_from_bytes(open('bytes.txt', 'wb'). ())
#for page in pages:
#    page.save('out.jpg', 'JPEG')

if __name__ == "__main__":
    app.run(debug=True)