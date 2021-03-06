import wave
import functools
import math
import numpy as np
import random
from random import shuffle
from Cipher import VigenereExtended
"""
  Package for encrypting and decrypting information in WAV files.
"""
__author__ = "Azis Adi Kuncoro"


def validateWAV(func):
    """
      Validation logic of every functions in WAV engine
    """
    @functools.wraps(func)
    def validate_init(*args, **kwargs):
        print("arg len: ", len(args))
        print("kwargs: ", kwargs["filePath"])
        if (len(args) != 2 and (not "filePath" in kwargs)):
            raise SystemExit(
                "[%s Error] you haven't provide a file" % func.__name__)
        else:
            path = kwargs["filePath"] if "filePath" in kwargs else args[1]
            if(path.split('.')[-1].lower() != "wav"):
                raise SystemExit(
                    "[%s Error] Only supports WAV type" % func.__name__)
        return func(*args, **kwargs)

    @functools.wraps(func)
    def validate(*args, **kwargs):
        if (args[0].container == None):
            raise SystemExit(
                "[%s Error] you haven't provide a file" % func.__name__)
        # elif (func.__name__ == "__encryptBytes"):
        #     if (type(args[1]) != bytes):
        #         raise SystemExit(
        #             "[%s Error] bytes argument doesn't have type byte" % func.__name__)
        #     elif (len(args[0].container) < len(args[1])):
        #         raise SystemExit(
        #             "[%s Error] data length larger than container" % func.__name__)

        return func(*args, **kwargs)

    if (func.__name__ == "__init__"):
        return validate_init
    else:
        return validate


class WavStegoEngine:
    """
      Main WAV stego class for encrypt and decrypt
    """
    container = None

    @validateWAV
    def __init__(self, filePath=None):
        ext = filePath.split('.')[-1]
        self.targetPath = ".".join(filePath.split('.')[:-1])+"_encrypted."+ext
        f = wave.open(filePath, mode="rb")
        self.params = f.getparams()
        self.container = f.readframes(f.getnframes())
        f.close()

    @validateWAV
    def __str__(self):
        s = "Capacity %d bytes, " % len(self.container)
        return s + str(self.params)

    @validateWAV
    def __encryptBytes(self, message_file_format, f_bytes, N_FRAMES, N_CHANNELS,stego_key, isMessageEncrypted, isRandomSequence):
        new_bytes = bytearray(self.container)
        print("Encrypted: {}, Shuffled: {}".format(isMessageEncrypted,isRandomSequence))
        bytes_per_frame = len(self.container)//N_FRAMES
        steps = bytes_per_frame // N_CHANNELS

        pos_li = [i*steps+(steps-1) for i in range(N_FRAMES*N_CHANNELS)]
        print("Len pos_li :",len(pos_li))

        
        #Write Encoding for MessageEncrypted and RandomSequence
        codeMessage = 2 if isMessageEncrypted else 0
        codeRandom = 1 if isRandomSequence else 0
        new_bytes[pos_li[0]] = ((new_bytes[pos_li[0]] & ~3) | (codeMessage | codeRandom))

        # Write formats LSB+1 == 0
        ext_format = message_file_format

        data_size = (8*len(ext_format)+8*len(f_bytes)+2)
        if (len(pos_li) < (data_size)):
            msg = "Error, Capacity: {}. But data: {}".format(len(pos_li),data_size)
            return (False, msg)

        form_li = pos_li[1:len(ext_format)*8+1]
        byte_to_write = [0 if c == '0' else 1 for c in "".join(
            [format(f_b, "08b") for f_b in bytes(ext_format, "utf-8")])]
        
    
        for i in range(len(byte_to_write)):
            new_bytes[form_li[i]] = (
                (new_bytes[form_li[i]] & ~3) | byte_to_write[i])

        # Write last format tag
        new_bytes[pos_li[1+len(ext_format)*8]] = (new_bytes[pos_li[1+len(ext_format)*8]] & ~3) | 3 

        # Write datas LSB == 1
        data_li = pos_li[2+len(ext_format)*8:].copy()

        

        if (isRandomSequence):
            sums = sum([ord(c) for c in stego_key])
            random.seed(sums)
            shuffle(data_li)
        if (isMessageEncrypted):
            f_bytes = VigenereExtended(key=stego_key).encrypt(f_bytes)


        byte_to_write = [2 if c == '0' else 3 for c in "".join(
            [format(f_b, "08b") for f_b in f_bytes])]
        for i, pos in enumerate(data_li):
            if (i < len(byte_to_write)):
                new_bytes[pos] = (
                    (new_bytes[pos] & ~3) | byte_to_write[i])
            else:  # Other, LSB+1 and LSB == 0
                new_bytes[pos] = new_bytes[pos] & ~3


        return (True, new_bytes)

    @validateWAV
    def __decryptFormatAndBytes(self, f_bytes, N_FRAMES, N_CHANNELS, stego_key):

        bytes_per_frame = len(f_bytes)//N_FRAMES
        steps = bytes_per_frame // N_CHANNELS
        pos_li = [i*steps+(steps-1) for i in range(N_FRAMES*N_CHANNELS)]


        ext_format = None
        read_bytes = []
        
        # Read Encoding for MessageEncrypted and RandomSequence
        isMessageEncrypted = True if ((f_bytes[pos_li[0]] & 2) == 2) else False
        isRandomSequence = True if ((f_bytes[pos_li[0]] & 1) == 1) else False

        
        # Read formats LSB+1 = 0
        end_pos_id = 1
        for i,pos in enumerate(pos_li[1:]):
            if (f_bytes[pos] & 2 == 2):
                end_pos_id = i + end_pos_id
                break
            else: pass


        b_str = "".join([str(f_bytes[pos] & 1)
                         for pos in pos_li[1:end_pos_id]])
        b_fmt = bytes([int(b_str[i:i+8], 2) for i in range(0, len(b_str), 8)])
        ext_format = b_fmt.decode("utf-8")

        data_li = pos_li[2+len(ext_format)*8:].copy()
        if (isRandomSequence):
            sums = sum([ord(c) for c in stego_key])
            random.seed(sums)
            shuffle(data_li)

        # Read datas
        msg_len = 0
        for i,pos in enumerate(data_li):
            if (f_bytes[pos] & 2 == 0):
                msg_len = i
                break

        b_str = "".join([str(f_bytes[pos] & 1) for pos in data_li[:msg_len]])
        read_bytes = bytes([int(b_str[i:i+8], 2) for i in range(0, len(b_str), 8)])
        # print("File bytes read: ",read_bytes.decode("utf-8"))
        
        if (isMessageEncrypted):
            read_bytes = VigenereExtended(key=stego_key).decrypt(read_bytes)


        return ext_format, read_bytes

    def __createWAVFile(self, targetPath, f_bytes, channel, samp_width, frame_rate, nframe, comp_type, comp_name):
        f = wave.open(targetPath, "wb")
        f.setnchannels(channel)
        f.setsampwidth(samp_width)
        f.setframerate(frame_rate)
        f.setnframes(nframe)
        f.setcomptype(comp_type, comp_name)
        f.writeframes(f_bytes)
        f.close()

    def __createDecryptedMsgFile(self, filePath, f_bytes):
        f = open(filePath, "wb")
        data_bytes = f.write(f_bytes)
        f.close()

    def encryptFile(self, filePath, stegoKey, isMessageEncrypted, isRandomSequence):
        f = open(filePath, "rb")
        data_bytes = f.read()
        print("Bytes length: ", len(data_bytes))
        message_file_format = filePath.split('.')[-1]
        status, encrypted_bytes = self.__encryptBytes(
            message_file_format=message_file_format, f_bytes=data_bytes, N_FRAMES=self.params[3], N_CHANNELS=self.params[0],
            stego_key=stegoKey, isMessageEncrypted=isMessageEncrypted, isRandomSequence=isRandomSequence)
        if (not status):
            message = encrypted_bytes
            return (status, message)
        self.__createWAVFile(targetPath=self.targetPath, f_bytes=encrypted_bytes, channel=self.params[0], samp_width=self.params[1],
                             frame_rate=self.params[2], nframe=self.params[3], comp_type=self.params[4], comp_name=self.params[5])
        f.close()
        return (status, self.targetPath)

    def decryptFile(self, filePath, outputPath, stego_key):
        f = wave.open(filePath, "rb")
        data_bytes = f.readframes(f.getnframes())
        ext_fmt, dec_bytes = self.__decryptFormatAndBytes(
            data_bytes, N_FRAMES=self.params[3], N_CHANNELS=self.params[0], stego_key=stego_key)
        filePath = outputPath+"/out."+ext_fmt
        self.__createDecryptedMsgFile(filePath,dec_bytes)
        f.close()
        return filePath

def compareWAVPSNR(oriPath, encPath):
    f_ori = wave.open(oriPath,"rb")
    ori_bytes = f_ori.readframes(f_ori.getnframes())
    N_CHANNELS = f_ori.getnchannels()
    N_FRAMES = f_ori.getnframes()
    f_ori.close()
    f_enc = wave.open(encPath,"rb")
    enc_bytes = f_enc.readframes(f_enc.getnframes())
    f_enc.close()
    psnr = countWAVPSNR(ori_bytes,enc_bytes,N_FRAMES,N_CHANNELS)
    print("PSNR: ",psnr)
    return psnr


def countWAVPSNR(ori_bytes, enc_bytes, N_FRAMES, N_CHANNELS):
    bytes_per_frame = len(ori_bytes)//N_FRAMES
    bytes_per_channel = bytes_per_frame // N_CHANNELS
    MAX_I = 2**(8*bytes_per_channel) - 1
    
    ori_segmented_bytes = []
    enc_segmented_bytes = []
    for i in range(0,len(ori_bytes),bytes_per_channel):
        z_ori = 0
        z_enc = 0
        for j in range(bytes_per_channel):
            z_ori = (z_ori << 8) | int(ori_bytes[i+j])
            z_enc = (z_enc << 8) | int(enc_bytes[i+j])
        ori_segmented_bytes.append(z_ori)
        enc_segmented_bytes.append(z_enc)
    ori_segmented_bytes = np.array(ori_segmented_bytes)
    enc_segmented_bytes = np.array(enc_segmented_bytes)
    _sum = np.sum((ori_segmented_bytes-enc_segmented_bytes)**2)
    MSE = _sum/(len(ori_segmented_bytes))
    print("Sum: ",_sum)
    print("MAX_I: %d. MSE: %d" %(MAX_I,MSE))
    print("BASE: ",20*math.log(MAX_I,10))
    psnr = 20*math.log(MAX_I,10) - 10*math.log(MSE,10)
    return psnr