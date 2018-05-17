from PIL import Image

def load_secret_image(source="politechnika.bmp"):
    image = Image.open(source)
    x_len, y_len = image.size

    pixel_list = []

    for i in range(0, y_len):
        for j in range(0, x_len):
            pixel = image.getpixel((j, i))
            pixel_list.append('{0:08b}'.format(pixel))

    return pixel_list

def calculate_new_indexes(x_len, y_len, old_x_indx, old_y_indx):
    if old_x_indx == x_len-1:
        x_indx = 0
        y_indx = old_y_indx + 1
    else:
        x_indx = old_x_indx + 1
        y_indx = old_y_indx
    return x_indx, y_indx

if __name__ == "__main__":
    pixel_list = load_secret_image()

    image = Image.open("duck.bmp")
    x_len, y_len = image.size

    x_indx = 0
    y_indx = 0

    color_list = []
    index_list = []

    for pixel in pixel_list:
        for i in range(0, 3):
            index_list.append((x_indx, y_indx))
            r, g, b = image.getpixel((x_indx, y_indx))
            color_list.append('{0:08b}'.format(r))
            color_list.append('{0:08b}'.format(g))
            color_list.append('{0:08b}'.format(b))
            x_indx, y_indx = calculate_new_indexes(x_len, y_len, x_indx, y_indx)

        #faza podmiany
        for i in range(0, 9):
            if i < 8:
                #ostatni element listy color_list jest pomijany
                tmp_color_value = list(color_list[i])
                tmp_color_value[7] = pixel[i]
                color_list[i] = "".join(tmp_color_value)
            color_list[i] = int(color_list[i], 2)

        #faza kodowania
        for i in range (0, 3):
            rgb = tuple(color_list[0:3])
            del color_list[0:3]
            image.putpixel(index_list.pop(0), rgb)

    image.save("duck-crypt.bmp")
