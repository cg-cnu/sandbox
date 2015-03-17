# need to download and install python image library (pil)

# currently hardcoded
# get a list of selected jpgs in the folder
# convert them to pdf in the same name


### todo: PHOTOSEVA ###############################################
# convert jpg to pdf
# convert pdf to jpg
# convert multiple pdfs/imgs to single pdf

# get the passport size photo from the scan
# scaling tools
# cloning tools
# 
###################################################################

import os, Image

desktop = "C:\Documents and Settings\Administrator\Desktop\jpg2pdf\\"
jpgs = [file for file in os.listdir(desktop)if file.endswith('.jpg')]    
jpegs = [file for file in os.listdir(desktop)if file.endswith('.jpeg')]


# get only jpegs
ji = jpgs + jpegs

# open the file with pil
for j in ji:    
    old_file = desktop + j
    tmp_img = Image.open(old_file)
    name = j.split('.')[0]
    tmp_img.save(desktop + name + ".pdf")
    os.remove(old_file)
