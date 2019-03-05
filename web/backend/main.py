from flask import Flask, request
from flask_cors import CORS, cross_origin
from WavStegoEngine import WavStegoEngine, compareWAVPSNR
from Cipher import VigenereExtended

app = Flask(__name__, static_folder='static', static_url_path='/static')
app.config['CORS_HEADERS'] = 'Content-Type'
cors = CORS(app)


host = "http://localhost:5000"

@app.after_request
def add_header(r):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.
    """
    r.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    r.headers["Pragma"] = "no-cache"
    r.headers["Expires"] = "0"
    r.headers['Cache-Control'] = 'public, max-age=0'
    return r


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
    # print("msg enc type: ", type(request.form['messageEncryption']))
    # if (bool(request.form['messageEncryption'])):
    #     buf = VigenereExtended(key=request.form['stegoKey']).encrypt(buf)

    createFile(containerPath, f_file.read())
    createFile(inputPath, buf)

    encrypted = True if request.form['messageEncryption'] == "true" else False
    randomSeq = True if request.form['randomSequence'] == "true" else False
    # Stego Engine Job
    engine = WavStegoEngine(filePath=containerPath)
    status, outPath = engine.encryptFile(filePath=inputPath,
        stegoKey=request.form['stegoKey'],
        isMessageEncrypted=encrypted,
        isRandomSequence=randomSeq)
    
    psnr = ""
    if (not status):
        message = outPath
        return message, 500
    else :
        psnr = str(compareWAVPSNR(containerPath, outPath))


    outPath = "/".join(outPath.split('/')[1:])
    paths = host+"/"+containerPath+"|"+host+"/"+outPath+"|"+psnr
    return paths, 200


@app.route('/decrypt', methods=['POST'])
def decrypt():
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
