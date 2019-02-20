from libs.WavStegoEngine import WavStegoEngine, compareWAVPSNR

if __name__ == "__main__":
    containerPath = "./samples/tone.wav"
    inputPath = "./inputfiles/gambar.jpg"
    encryptPath = "./samples/tone_encrypted.wav"
    
    engine = WavStegoEngine(filePath=containerPath)

    # print(engine)
    engine.encryptFile(filePath=inputPath)
    engine.decryptFile(filePath=encryptPath)

    compareWAVPSNR(containerPath,encryptPath)