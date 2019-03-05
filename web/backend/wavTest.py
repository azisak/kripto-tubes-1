from WavStegoEngine import WavStegoEngine


def decryptionTest(containerPath, stegoKey):
    outPath = "./static"
    engine = WavStegoEngine(filePath=containerPath)
    outPath = engine.decryptFile(
        filePath=containerPath,
        outputPath=outPath,
        stego_key=stegoKey
    )

    print("Done, Outpath: ",outPath)
    return outPath

def encryptionTest(containerPath, inputPath, stegoKey):
    encrypted, randomSeq = True, True

    engine = WavStegoEngine(filePath=containerPath)
    status, outPath = engine.encryptFile(
        filePath=inputPath,
        stegoKey=stegoKey,
        isMessageEncrypted=encrypted,
        isRandomSequence=randomSeq)
    
    if (not status):
        message = outPath
        print("Error, Message: ",message)
        assert False
    else:
        print("Done, output in: ",outPath)
        return outPath
    # engine.decryptFile(filePath=encryptPath)

    # compareWAVPSNR(containerPath,encryptPath)


if __name__ == "__main__":
    stegoKey = "YOLOOO"

    containerPath = "./static/instrument.wav"
    inputPath = "./static/apa.txt"
    outPath = "./static/instrument_encrypted.wav"

    outPath =  encryptionTest(containerPath, inputPath, stegoKey)

    print("\n\nEncryption DONE\n\n")
    
    outPath = decryptionTest(outPath,stegoKey)
