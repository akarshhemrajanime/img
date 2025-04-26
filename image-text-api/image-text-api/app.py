from PIL import Image, ImageDraw, ImageFont
import requests
from io import BytesIO
from flask import Flask, request, send_file

app = Flask(__name__)

@app.route('/generate-image', methods=['GET'])
def generate_image():
    text = request.args.get('text')  # Ambil teks dari query parameter
    background_url = request.args.get('background_url')  # Ambil URL background
    
    if not text or not background_url:
        return "Missing required parameters", 400

    # Ambil gambar background dari URL
    response = requests.get(background_url)
    img = Image.open(BytesIO(response.content))

    # Setup font dan text
    draw = ImageDraw.Draw(img)
    font = ImageFont.load_default()  # Bisa diganti dengan font lain jika diperlukan

    # Tentukan posisi teks
    text_width, text_height = draw.textsize(text, font)
    x = (img.width - text_width) / 2
    y = img.height - text_height - 20  # Posisi teks di bawah

    draw.text((x, y), text, font=font, fill="white")

    # Simpan gambar hasil ke response
    img_io = BytesIO()
    img.save(img_io, 'JPEG')
    img_io.seek(0)

    return send_file(img_io, mimetype='image/jpeg')

if __name__ == '__main__':
    app.run(debug=True)
