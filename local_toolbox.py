import os
import time
import fitz
from pdfrw import PdfReader


def pdf_title(filepath):
    # Read title
    raw_title = PdfReader(filepath).Info.Title
    # Strip '(' and ')' and return
    return raw_title[1:-1]


def save_imgs(pdfpath, imgspath):
    # Extract and save images from pdf file
    # pdfpath: path of pdf file
    # imgspath: path of images in pdf file

    # Prepare imgspath, usually it doesnot exist
    if not os.path.exists(imgspath):
        os.mkdir(imgspath)

    # Open pdf file
    with fitz.open(pdfpath) as doc:
        # For each object
        for j in range(1, doc._getXrefLength()):
            # Try to read pixels and save them as image
            # This seems to be convenient for all possible images
            try:
                pix = fitz.Pixmap(doc, j)
                pix.writePNG(os.path.join(imgspath, 'img-{}.png'.format(j)))
            except:
                continue