def get_certificate(name):
  from PIL import Image, ImageDraw, ImageFont
  import pandas as pd
  from google.colab import files
  import os
  os.system("wget https://dl.dropboxusercontent.com/s/mxgxuqe9ejptl2k/Certificate.png -O Certificate.png --quiet")
  os.system("wget https://dl.dropboxusercontent.com/s/hpd7246qdczd5wq/bellania.ttf?dl=0 -O bellania.ttf --quiet")
  url = "https://drive.google.com/uc?export=download&id=1MUlHNAjZ_n40ciSW4f0enZgnz2AG5ilI"
  form = pd.read_excel(url)
  name_list = form['Name'].to_list()
  if name in name_list:
    im = Image.open("Certificate.png")
    d = ImageDraw.Draw(im)
    # location = (360, 350)
    W, H = (960, 750)
    # text_color = (0, 0, 0)
    font = ImageFont.truetype("bellania.ttf", 25)
    w,h = font.getsize(name)
    d.text(((W-w)/2,(H-h)/2), name, font=font, fill="black")
    # d.text(location, name, fill=text_color, font=font)
    im.save(f"certificate_{name}.pdf")
    print(f"Congratulations {name}, your certificate is ready!")
    files.download(f"certificate_{name}.pdf")
  else:
    print("Sorry, the name you entered is not in the spreadsheet.")
