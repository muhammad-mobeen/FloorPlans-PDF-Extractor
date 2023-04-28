# from boopnet import extract_from_pdf, extract_all_from_directory
from pdf2image import convert_from_path
import os
import shutil # to save it locally

''' 
First we need to do following:
a) Convert PDF to images first
'''

# extract_all_from_directory("talk\\test")
# extract_from_pdf("fp.pdf")
# extract_from_pdf("1 2.pdf")

class PDF_to_Floor_Plans:
    def __init__(self, pdf_path, dpi, destination_folder) -> None:
        self.pdf_path = pdf_path
        self.destination_folder = destination_folder
        self.dpi = dpi

    def dirManager(self, dir, mode=None):
        if mode == "replace":
            if os.path.exists(dir):
                shutil.rmtree(dir)
            os.makedirs(dir)
        else:
            if not os.path.exists(dir):
                os.makedirs(dir)

    def pdf2images(self):
        print("Initializing PDF2Image Conversion!")
        pages = convert_from_path(self.pdf_path, self.dpi)

        #Saving pages in jpeg format
        for i,page in enumerate(pages):
            image_name = "{}/{}__page__{}.png".format(self.destination_folder,"fp",i)
            try:
                page.save(image_name, 'png')
                print("{} saved successfully!".format(image_name))
            except Exception as e:
                print("Could not save image: {}\nFollowing error occured: {}".format(image_name, e))

        print("PDF2Image Operation Completed!")

    def detect_images(self):
        



if __name__ == '__main__':
    agent = PDF_to_Floor_Plans('fp.pdf', 300, 'Images')
    agent.pdf2images()