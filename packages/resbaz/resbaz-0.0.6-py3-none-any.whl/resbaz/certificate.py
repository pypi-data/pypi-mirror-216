from PIL import Image, ImageDraw, ImageFont
import pandas as pd
from google.colab import files
import os


def get_certificate(name):
    os.system("wget https://dl.dropboxusercontent.com/s/9j139opcgwfwb3z/Certificate.jpg -O Certificate.jpg --quiet")
    os.system("wget https://dl.dropboxusercontent.com/s/hpd7246qdczd5wq/bellania.ttf?dl=0 -O bellania.ttf --quiet")
    url = "https://drive.google.com/uc?export=download&id=1MUlHNAjZ_n40ciSW4f0enZgnz2AG5ilI"
    form = pd.read_excel(url)
    name_list = form['Name'].to_list()
    if name in name_list:
        im = Image.open("Certificate.jpg")
        d = ImageDraw.Draw(im)
        W, H = (1289, 998)
        font = ImageFont.truetype("bellania.ttf", 35)
        w, h = font.getsize(name)
        d.text(((W-w)/2, (H-h)/2), name, font=font, fill="black")
        im.save(f"certificate_{name}.pdf")
        print(f"Congratulations {name}, your certificate is ready!")
        files.download(f"certificate_{name}.pdf")
    else:
        print("Sorry, the name you entered is not in the spreadsheet.")
