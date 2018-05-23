from PIL import Image

def load_source_image(path):
    image = Image.open(path)
    size = image.size
    pixel_list = list(image.getdata())
    return size, pixel_list

def load_secret_image(path):
    image = Image.open(path)
    size = image.size
    pixel_list = list(image.getdata())
    palette = image.getpalette()
    return size, pixel_list, palette

def encrypt_part(source_pixel_list, secret_part, source_index=0):
    #secret_part is either palette or secret image pixel list

    color_list = []
    index_list = []

    for value in secret_part:
        binary_value = '{0:08b}'.format(value)

        #fetching 3 next pixels of source image
        for i in range(0,3):
            index_list.append(source_index)
            r, g, b = source_pixel_list[source_index]
            color_list.append('{0:08b}'.format(r))
            color_list.append('{0:08b}'.format(g))
            color_list.append('{0:08b}'.format(b))
            source_index += 1

        #changing the last bit of source pixels
        for i in range(0, 9):
            if i < 8:
                #the last element of the color_list is omitted
                tmp_color_value = list(color_list[i])
                tmp_color_value[7] = binary_value[i]
                color_list[i] = "".join(tmp_color_value)
            color_list[i] = int(color_list[i], 2)

        #save results in list of source image pixels
        for i in range (0, 3):
            rgb = tuple(color_list[0:3])
            del color_list[0:3]
            source_pixel_list[index_list.pop(0)] = rgb

    return source_pixel_list, source_index

def encrypt(source_image_path, secret_image_path):
    source_image_size, source_pixel_list = load_source_image(source_image_path)
    secret_image_size, secret_pixel_list, secret_palette = load_secret_image(secret_image_path)

    #encrypting the palette
    source_pixel_list, source_index = encrypt_part(source_pixel_list, secret_palette)

    #encrypting the pixels
    source_pixel_list, source_index = encrypt_part(source_pixel_list, secret_pixel_list, source_index)

    encrypted_image = Image.new("RGB", source_image_size)
    encrypted_image.putdata(source_pixel_list)
    encrypted_image.save("duck-crypt.bmp")

    return (secret_image_size[0], secret_image_size[1], len(secret_palette))

if __name__ == "__main__":
    # Key can be used to reveal the secret image. It can be also sent to a receiver
    # using the RSA cryptography.
    key = encrypt("duck.bmp", "politechnika.bmp")
