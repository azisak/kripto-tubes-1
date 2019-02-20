from flask import Flask, request
from flask_cors import CORS, cross_origin
from WavStegoEngine import WavStegoEngine
from Cipher import VigenereExtended

app = Flask(__name__, static_folder='static', static_url_path='/static')
app.config['CORS_HEADERS'] = 'Content-Type'
cors = CORS(app)


host = "http://localhost:5000"


@app.route('/encrypt', methods=['POST'])
def encrypt():
    print("Data:")
    print(request.form)
    print(request.form['stegoKey'])
    print(request.form['randomSequence'])
    print(request.form['messageEncryption'])
    f_file = request.files['containerFile']
    f_msg = request.files['messageFile']
    containerPath = "./static/%s" % (f_file.filename)
    inputPath = "./static/%s" % (f_msg.filename)

    buf = f_msg.read()
    print("msg enc type: ", type(request.form['messageEncryption']))
    if (bool(request.form['messageEncryption'])):
        buf = VigenereExtended(key=request.form['stegoKey']).encrypt(buf)

    createFile(containerPath, f_file.read())
    createFile(inputPath, buf)

    # Stego Engine Job
    engine = WavStegoEngine(filePath=containerPath)
    outPath = engine.encryptFile(filePath=inputPath,
        stegoKey=request.form['stegoKey'],
        isMessageEncrypted=bool(request.form['messageEncryption']),
        isRandomSequence=bool(request.form['randomSequence']))

    outPath = "/".join(outPath.split('/')[1:])
    print("Outpah")
    print(outPath)
    return (host+"/"+outPath), 200


@app.route('/decrypt', methods=['POST'])
def decrypt():
    print("Data:")
    print(request.form['stegoKey'])
    f_file = request.files['containerFile']

    containerPath = "./static/%s" % (f_file.filename)
    outputPath = "/".join(containerPath.split('/')[:-1])

    createFile(containerPath, f_file.read())

    # Stego Engine Job
    engine = WavStegoEngine(filePath=containerPath)
    outPath = engine.decryptFile(
        filePath=containerPath, outputPath=outputPath, stego_key=request.form['stegoKey'])

    outPath = "/".join(outPath.split('/')[1:])
    return (host+"/"+outPath), 200


def createFile(filePath, fileBytes):
    f = open(filePath, "wb")
    f.write(fileBytes)
    f.close()
