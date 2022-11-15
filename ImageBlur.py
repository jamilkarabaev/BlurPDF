from PIL import ImageFilter, Image
import zlib, tqdm, os, pdfplumber, fitz, cv2
from pdf2image import convert_from_path
import numpy as np
from fpdf import FPDF

#params
target_pdf = "1611.07004.pdf"
blur_level = 15

def create_images():
    """function to extract images from the PDF"""
    target_pdf = "1611.07004.pdf"
    document = fitz.Document((target_pdf))
    for i in range(len(document)):
        # print(document[i].get_image_info()[:][:]['bbox'])
        page = document[i].get_pixmap()  # render page to an image
        page_folder = 'C:/Users/Jamil PC/Desktop/BlurPDF/{}/'.format(target_pdf[:-3])
        if not os.path.isdir(page_folder):
            os.mkdir(page_folder)
        page.save(os.path.join(page_folder, "%i.png" % i))
        page_image = cv2.imread(os.path.join(page_folder, "%i.png" % i))
        for x in range(len(document.get_page_images(i))):
            xref = document.get_page_images(i)[x][0]
            image = document.extract_image(xref)
            pix = fitz.Pixmap(document, xref)
            image_folder = 'C:/Users/Jamil PC/Desktop/BlurPDF/{}-images'.format(target_pdf[:-3])
            if not os.path.isdir(image_folder):
                os.mkdir(image_folder)
            pix.save(os.path.join(image_folder, "p%s-%s.png" % (i, xref)))
            bbox = document[i].get_image_bbox(document.get_page_images(i, full=True)[x])
            # print(bbox.__dict__)
            x, y = int(bbox.x0) , int(bbox.y0)
            w, h = int(bbox.x1) - int(bbox.x0), int(bbox.y1) - int(bbox.y0)
            print(x , y, w, h)
            ROI = page_image[y:y+h, x:x+w]
            blur = cv2.GaussianBlur(ROI, (151,151), 0)
            page_image[y:y+h, x:x+w] = blur
        cv2.imwrite(os.path.join(page_folder, "%i.png" % i), page_image) 

def stitch():
    image_list = os.listdir('C:/Users/Jamil PC/Desktop/BlurPDF/{}/'.format(target_pdf[:-3]))
    images = [
        Image.open('C:/Users/Jamil PC/Desktop/BlurPDF/{}/'.format(target_pdf[:-3]) + f)
        for f in image_list
    ]
    print(images)
    print(len(images))
    pdf_path = "C:/Users/Jamil PC/Desktop/BlurPDF/{}_done.pdf".format(target_pdf[:-3])
    images[0].save(
    pdf_path, "PDF" ,resolution=100.0, save_all=True, append_images=images[1:]
    )

def produce_blurred_images():
    image_folder = 'C:/Users/Jamil PC/Desktop/BlurPDF/{}-images/'.format(target_pdf[:-3])
    image_list = os.listdir(image_folder)
    destination_folder = 'C:/Users/Jamil PC/Desktop/BlurPDF/{}-images-blurred/'.format(target_pdf[:-3])
    if not os.path.isdir(destination_folder):
        os.mkdir(destination_folder)
    for image in image_list:
        OriImage = Image.open(image_folder + image).convert('L')
        gaussImage = OriImage.filter(ImageFilter.GaussianBlur(blur_level))
        gaussImage.save(destination_folder + image)

if __name__ == '__main__':
    create_images()
    stitch()
    # produce_blurred_images()


# full_page_image = cv2.imread('full_page_image.jpg')
# image_to_be_added = cv2.imread('boat.jpg')
# final_image = full_page_image.copy()
# final_image[100:400,100:400,:] = image_to_be_added[100:400,100:400,:] #adjust the numbers according to the dimensions of the image_to_be_added
# cv2.imwrite(final_image.jpg, final_image)
