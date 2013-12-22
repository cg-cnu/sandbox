import Image
import pyPdf
import os

PATH = "/home/salapati/Desktop/testPhoto/"

FORMATS = ['jpg', 'jpeg', 'png','tga','tif']

SELECTION = [photo for photo in os.listdir(PATH)]

photos = [phot for photo in SELECTION if str(photo.split('.')[-1]) in FORMATS]
pdfs = []

for photo in photos:
	size = os.path.getsize( PATH + phot)
	while size >= fileSize:
        tmpImg = Image.open(PATH + photo)
        tmpImg.save(PATH + name + '.pdf')
		size = os.path.getsize(PATH + photo)

# conv to pdf		
for photo in photos:
	tmpImg = Image.open(PATH + photo)
	name = photo.split(".")[0]
	tmpImg.save(PATH + pdf + ".pdf")
	pdfs.append(name + ".pdf")
	os.remove(PATH + photo)
	
OUTPUT = pyPdf.PdfFileWriter()

for pdf in PDFS:
	pdfTmp = pyPdf.PdfFileReader(file(PATH + pdf))
    noOfPages = int(pdfTmp.numPages)
    if noOfPages > 1:
    	for i in range(0, noOfPages):
        	OUTPUT.addPage(pdftmp.getPage(i))
	else:
    	OUTPUT.addPage(pdfTmp.getPage(0))
	os.remove(PATH + pdf)
	
outputStream = file(PATH + "combined_1.pdf", "wb")
OUTPUT.write(outputStream)
outputStream.close()
