from PIL import Image

class SteganoBitmap:
    def __init__(self, key, israndom):
        self.cipher_key = key.lower()
        if (israndom):
            self.israndom = True
            self.seed = self.calculate_seed(key.lower())

    def hide(self, img_path, message):
        img = Image.open(img_path)
        pixel_array = self.get_pixel_array(img)

        j = 0
    
        print('ori : {0}'.format(pixel_array[j]))
        
        message_byte = message.encode("utf-8")
        
        print('this is byte {0}'.format(message_byte))
        message_hex = message_byte.hex()
        print('this is hex {0}'.format(message_hex))
        message_bin = bin(int(message_hex, 16))[2:].zfill(8 * (len(message_hex)//2))
        print('msg : {0} and length : {1}'.format(message_bin, len(message_bin)))
        hiding_method = '01'
        message_to_hide = hiding_method + message_bin

        print('msg : {0} and length : {1}'.format(message_to_hide, len(message_to_hide)))

        for i in range(0, len(pixel_array)):
            pixel_array[i] = list(pixel_array[i])

        for i in range(0, len(message_to_hide)):
            channel = pixel_array[i//3][i%3]
            pixel_array[i//3][i%3] = self.modify_lsb(channel, message_to_hide[i])    

        for i in range(0, len(pixel_array)):
            pixel_array[i] = tuple(pixel_array[i])

        print('mod : {0}'.format(pixel_array[j]))

        img.putdata(pixel_array)
        img.save('out/stego.bmp')

    def extract(self, img_path):
        img = Image.open(img_path)
        pixel_array = self.get_pixel_array(img)

        extracted_bin = ''
        for i in range(2, 58):
            extracted_bin += bin(pixel_array[i//3][i%3])[-1:]

        print('{0} and {1}'.format(extracted_bin, len(extracted_bin)))
        extracted_hex = ''
        for i in range(0, len(extracted_bin)//8):
            print('hey : {0}'.format(extracted_bin[8*i:(8*i)+8]))
            extracted_hex += hex(int(extracted_bin[8*i:8*i+8],2))[2:]
        print(extracted_hex)
        extracted = bytes.fromhex(extracted_hex)
        return extracted.decode('utf-8')

    def get_pixel_array(self, img):
        width, height = img.width, img.height
        pixel_array = [img.getpixel((row, col)) for col in range(0, height) for row in range(0, width)]
        return pixel_array

    def modify_lsb(self, to_modify, bit_to_insert):
        modified = to_modify
        if bit_to_insert == '0':
            if modified % 2 != 0:
                modified = modified - 1
        else:
            if modified % 2 == 0:
                modified = modified + 1
        return modified


    def calculate_seed(self, key):
        seed = 0
        for c in key:
            seed = seed + ord(c) - 96
        return seed
