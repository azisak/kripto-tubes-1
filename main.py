from libs.Stegano import SteganoBitmap


def main():
    stegano = SteganoBitmap('Key', False)
    stegano.hide('samples/jazzstops.bmp', 'abcXYZ~')

    res = stegano.extract('out/stego.bmp')

    print(res)

main()