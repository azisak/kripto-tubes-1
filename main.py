from libs.Stegano import SteganoBitmap


def main():
    stegano = SteganoBitmap()
    print(stegano.get_capacity('samples/jazzstops.bmp'))
    stegano.hide('samples/jazzstops.bmp', 'abcXYZ~')

    res = stegano.extract('out/stego.bmp')

    print(res)

main()