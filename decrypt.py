from PIL import Image

if __name__ == "__main__":
    #kluczem do odszyfrowania jest para liczb x_indx, y_indx
    image = Image.open("duck-crypt.bmp")
    test_image = Image.open("politechnika.bmp")
    img_palette = test_image.getpalette()
    # print(len(img_palette))
    # print(img_palette)
    x_len, y_len = image.size
    x_indx, y_indx = 512, 500

    single_color = []
    secret_image_pixel_list = []

    for i in range(0, y_indx+1):
        for j in range(0, x_len):
            if i == y_indx and j == x_indx:
                break
            r, g, b = image.getpixel((j, i))
            r_byte = ('{0:08b}'.format(r))
            g_byte = ('{0:08b}'.format(g))
            b_byte = ('{0:08b}'.format(b))
            if len(single_color) == 6:
                #z poprzednich dwóch iteracji
                single_color.append(r_byte[-1])
                single_color.append(g_byte[-1])
                pixel_string = ''.join(single_color)
                secret_image_pixel_list.append(int(pixel_string, 2))
                single_color = []
                pixel_string = ''
            else:
                single_color.append(r_byte[-1])
                single_color.append(g_byte[-1])
                single_color.append(b_byte[-1])

    new_image = Image.new("P", (448, 298))
    new_image.putdata(secret_image_pixel_list)
    new_image.show()
