from PIL import Image

def load_stego_image(path):
    image = Image.open(path)
    pixel_list = list(image.getdata())
    return pixel_list

def decrypt_part(stego_pixel_list, stego_image_start_index, stego_image_end_index):
    #used to decrypt both palette and pixel list
    single_color = []
    secret_part = []

    for i in range(stego_image_start_index, stego_image_end_index):
            r, g, b = stego_pixel_list[i]
            r_byte = ('{0:08b}'.format(r))
            g_byte = ('{0:08b}'.format(g))
            b_byte = ('{0:08b}'.format(b))
            if len(single_color) == 6:
                #from two previous iterations
                single_color.append(r_byte[-1])
                single_color.append(g_byte[-1])
                pixel_string = ''.join(single_color)
                secret_part.append(int(pixel_string, 2))
                single_color = []
                pixel_string = ''
            else:
                single_color.append(r_byte[-1])
                single_color.append(g_byte[-1])
                single_color.append(b_byte[-1])

    return secret_part

def decrypt(key, stego_image_path="duck-crypt.bmp"):
    # In order to reveal the secret one has to pass size of the secret and the palette.
    # Those can be sent safely, for example, using RSA cryptography.
    secret_image_height = key[0]
    secret_image_width =  key[1]
    secret_image_palette_size = key[2]

    secret_image_size = secret_image_height * secret_image_width
    stego_pixel_list = load_stego_image(stego_image_path)

    stego_image_end_index = secret_image_palette_size*3
    secret_image_palette = decrypt_part(stego_pixel_list, 0, stego_image_end_index)

    stego_image_start_index = stego_image_end_index
    stego_image_end_index = stego_image_start_index + 3*secret_image_size
    secret_image_pixel_list = decrypt_part(stego_pixel_list, stego_image_start_index, stego_image_end_index)

    secret_image = Image.new("P", (secret_image_height, secret_image_width))
    secret_image.putdata(secret_image_pixel_list)
    secret_image.putpalette(secret_image_palette)
    secret_image.show()

if __name__ == "__main__":
    key = (448, 298, 768)
    # first - height of the secret image
    # second - width of the secret image
    # third - size of the palette

    decrypt(key)
