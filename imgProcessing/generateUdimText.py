from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

import random

startUdim = 1001
endUdim = 1020

imageSize = 256


path = "/home/salaati/Desktop/udims/"

for udim in range(startUdim, endUdim+1):

	rr = random.randint(0, 255)
	rg = random.randint(0, 255)
	rb = random.randint(0, 255)

	color = "rgb(%s,%s,%s)" %(rr, rg, rb)
	img = Image.new("RGB", (imageSize, imageSize),  color)

	draw = ImageDraw.Draw(img)
	font = ImageFont.truetype("/usr/share/fonts/dejavu/DejaVuSerif-Italic.ttf", 16)
	draw.text((imageSize/2, imageSize/2), "UDIM:"+str(udim), (0,0,0), font=font)

	img.save(path + "assetId.diffuse." + str(udim) + ".png", format="png")



# from PIL import ImageFont
# from PIL import ImageDraw 
# img = Image.open("sample_in.jpg")
# # font = ImageFont.truetype(<font-file>, <font-size>)
# # draw.text((x, y),"Sample Text",(r,g,b))
# >>> img.save('sample-out.jpg')