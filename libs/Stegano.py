from PIL import Image
from os.path import basename
import binascii

class SteganoBitmap:
    def __init__(self, signature='stg'):
        self.signature_bin = self.string_to_bin(signature)

    def get_capacity(self, img_path):
        img = Image.open(img_path)
        pixel_array = self.get_pixel_array(img)
        img.close()

        capacity = len(pixel_array) * len(pixel_array[0])
        
        return capacity

    def hide(self, img_path, message):
        img = Image.open(img_path)
        pixel_array = self.get_pixel_array(img)

        message_to_hide = self.build_string_to_hide(True, message, '00')

        print('string built : {0}'.format(self.build_string_to_hide(True, message, '00')))

        for i in range(0, len(pixel_array)):
            pixel_array[i] = list(pixel_array[i])

        for i in range(0, len(message_to_hide)):
            channel = pixel_array[i//3][i%3]
            pixel_array[i//3][i%3] = self.modify_lsb(channel, message_to_hide[i])

        for i in range(0, len(pixel_array)):
            pixel_array[i] = tuple(pixel_array[i])

        img.putdata(pixel_array)
        img.save('out/stego.bmp')
        img.close()

    def extract(self, img_path):
        img = Image.open(img_path)
        pixel_array = self.get_pixel_array(img)

        extracted_bin = ''
        for i in range(0, self.get_capacity(img_path)):
            extracted_bin += bin(pixel_array[i//3][i%3])[-1:]

        # check signature
        signature_length = len(self.signature_bin)
        extracted_signature = extracted_bin[: signature_length]
        if extracted_signature == self.signature_bin:
            # check hiding method
            extracted_hiding_method = extracted_bin[signature_length: signature_length + 2]
            if extracted_hiding_method == '00':
                # check is_string
                extracted_is_string = extracted_bin[signature_length + 2: signature_length + 4]
                if extracted_is_string == '01':
                    length_bin = extracted_bin[signature_length + 4: signature_length + 36]
                    length = int(length_bin, 2)
                    string_bin = extracted_bin[signature_length + 36: signature_length + 36 + (length * 8)]

                    extracted_string = binascii.unhexlify('%x' % (int(string_bin, 2)))

                    return extracted_string.decode('utf-8')

                elif extracted_is_string == '00':
                    return NotImplementedError()
                    # if no
                        # get file_path length
                        # get length
                        # get file_path
                        # get content
                        # build the file
                else:
                    return False
            else:
                return NotImplementedError()
        else:
            return False
    
    def build_string_to_hide(self, is_string, input_data, hiding_method):
        string_to_hide = ''
        string_to_hide += self.signature_bin
        string_to_hide += hiding_method
        if is_string:
            string_to_hide += '01'
            string_data = input_data
            #add length_in_bin 32b
            string_to_hide += bin(len(string_data))[2:].zfill(32)
            #add string
            string_to_hide += self.string_to_bin(string_data)
        else:
            string_to_hide += '00'
            file_path = input_data
            with open(file_path, 'rb') as f:
                file_byte = f.read()
            f.close()
            print('filebyte : {0}'.format(file_byte))
            #add filename_length_in_bin 16b
            string_to_hide += bin(len(file_path))[2:].zfill(16)
            #add length_in_bin 32b
            string_to_hide += bin(len(file_byte))[2:].zfill(32)
            #add filename
            string_to_hide += self.string_to_bin(basename(file_path))
            #add content
            content_hex = file_byte.hex()
            string_to_hide += bin(int(content_hex, 16))[2:].zfill(8 * (len(content_hex)//2))
        
        return string_to_hide

    def string_to_bin(self, input_data):
        string_byte = input_data.encode("utf-8")
        string_hex = string_byte.hex()
        return bin(int(string_hex, 16))[2:].zfill(8 * (len(string_hex)//2))

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
