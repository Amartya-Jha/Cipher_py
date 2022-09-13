import streamlit as st
from PIL import Image, ImageFont, ImageDraw
import textwrap
import base64

st.title('Text cipher')

input_text = st.text_input('Enter original text here')
method = st.selectbox('Select cipher method', ('Caesar','base64',))

if method == 'Caesar':
    result = ""
    cno = st.number_input('Enter shift number', step = 1)
    for i in range(len(input_text)):
        char = input_text[i]

        if (char.isupper()):
            result += chr((ord(char) + cno - 65) % 26 + 65)
        else:
            result += chr((ord(char) + cno - 97) % 26 + 97)
    st.write("Encoded text is: ", result)

if method == 'base64':
    asc_enc = input_text.encode("ascii")
    b64_enc = base64.b64encode(asc_enc)
    result = b64_enc.decode('ascii')
    st.write('Encoded string is: ', result)

#STEGANOGRAPHY
st.title('Steganography')

def load_image(image_file):
	img = Image.open(image_file)
	return img

uploaded_file = st.file_uploader("Upload Files",type=['png','jpeg','jpg'])

if uploaded_file is not None:
    file_details = {"FileName":uploaded_file.name,"FileType":uploaded_file.type,"FileSize":uploaded_file.size}
    st.write(file_details)

def write_text(result, image_size):
    """Writes text to an RGB image. Automatically line wraps

    text_to_write: the text to write to the image
    """
    image_text = Image.new("RGB", image_size)
    font = ImageFont.load_default().font
    drawer = ImageDraw.Draw(image_text)

    #Text wrapping. Change parameters for different text formatting
    margin = offset = 10
    for line in textwrap.wrap(result, width=60):
        drawer.text((margin,offset), line, font=font)
        offset += 10
    return image_text

def encode_image(result, uploaded_file):
    """Encodes a text message into an image

    text_to_encode: the text to encode into the template image
    template_image: the image to use for encoding. An image is provided by default.
    """
    uploaded_file = Image.open(uploaded_file)
    red_template = uploaded_file.split()[0]
    green_template = uploaded_file.split()[1]
    blue_template = uploaded_file.split()[2]

    x_size = uploaded_file.size[0]
    y_size = uploaded_file.size[1]

    #text draw
    image_text = write_text(result, uploaded_file.size)
    bw_encode = image_text.convert('1')

    #encode text into image
    encoded_image = Image.new("RGB", (x_size, y_size))
    pixels = encoded_image.load()
    for i in range(x_size):
        for j in range(y_size):
            red_template_pix = bin(red_template.getpixel((i,j)))
            old_pix = red_template.getpixel((i,j))
            tencode_pix = bin(bw_encode.getpixel((i,j)))

            if tencode_pix[-1] == '1':
                red_template_pix = red_template_pix[:-1] + '1'
            else:
                red_template_pix = red_template_pix[:-1] + '0'
            pixels[i, j] = (int(red_template_pix, 2), green_template.getpixel((i,j)), blue_template.getpixel((i,j)))
    st.image(encoded_image)
if st.button('Encode'):
    encode_image(result, uploaded_file)




