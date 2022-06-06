from PIL import Image, ImageFont, ImageDraw
import textwrap

def decode_image(file_location, file_to_save):
    encoded_image = Image.open(file_location)
    red_channel = encoded_image.split()[0]

    x_size = encoded_image.size[0]
    y_size = encoded_image.size[1]

    decoded_image = Image.new("RGB", encoded_image.size)
    pixels = decoded_image.load()

    for i in range(x_size):
        for j in range(y_size):
            if red_channel.getpixel((i, j)) & 1:
                pixels[i, j] = (255, 255, 255)
            else:
                pixels[i, j] = (0, 0, 0)

    decoded_image.save(file_to_save)

def write_text(text_to_write, image_size):
    image_text = Image.new("RGB", image_size)
    font = ImageFont.load_default().font
    drawer = ImageDraw.Draw(image_text)

    margin = offset = 10
    for line in textwrap.wrap(text_to_write, width=30):
        drawer.text((margin,offset), line, font=font)
        offset += 10
    return image_text

def encode_image(text_to_encode, template_image, file_to_save):
    template_image = Image.open(template_image)
    width = template_image.size[0]
    height = template_image.size[1]

    text_watermark = write_text(text_to_encode, template_image.size)
    text_watermark = text_watermark.convert(mode='1')

    encoded_image = Image.new("RGB", template_image.size)
    pixels = encoded_image.load()

    for x in range(width):
        for y in range(height):
            text_pixel = text_watermark.getpixel((x, y))
            img_pixel = template_image.getpixel((x, y))
            red = (img_pixel[0] >> 1) << 1
            red |= text_pixel & 1
            img_pixel = (red, *img_pixel[1:])
            pixels[x, y] = img_pixel

    encoded_image.save(file_to_save)

if __name__ == '__main__':
    print("Encoding the image...")
    encode_image('to jest przykladowa wiadomosc, blablabla, UG jest suuuuuper', 'house.png', 'encoded_img.png')

    print("Decoding the image...")
    decode_image('encoded_img.png', 'decoded_text.png')
