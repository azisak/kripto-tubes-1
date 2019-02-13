from libs.Stegano import SteganoBitmap


def main():
    stegano = SteganoBitmap()

    print(stegano.get_capacity('samples/jazzstops.bmp'))
    print(stegano.get_capacity('samples/past.bmp'))
    
    stegano.hide('samples/jazzstops.bmp', 'out/stego.bmp', True, 'abcXYZ~')
    stegano.hide('samples/past.bmp', 'out/stego2.bmp', False, 'samples/small.gif')

    res = stegano.extract('out/stego.bmp')
    res = stegano.extract('out/stego2.bmp')

main()