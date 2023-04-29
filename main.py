from boopnet import extract_from_pdf, extract_all_from_directory
from boopnet.utilities import preprocess, postprocess, segmentation_model
from inbac import inbac
from pdf2image import convert_from_path
from skimage import io
from skimage.util import img_as_ubyte
import os
import shutil # to save it locally

''' 
First we need to do following:
a) Convert PDF to images first
'''

# extract_all_from_directory("talk\\test")
# extract_from_pdf("fp.pdf")
# extract_from_pdf("1 2.pdf")

model = segmentation_model()

class PDF_to_Floor_Plans:
    def __init__(self, pdf_path, dpi, img_destination_folder, fp_destination_folder):
        self.pdf_path = pdf_path
        self.img_destination_folder = img_destination_folder
        self.fp_destination_folder = fp_destination_folder
        # self.user_destination_folder = user_destination_folder
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
        print("Converting PDF to Images..........")
        pages = convert_from_path(self.pdf_path, self.dpi)

        # Manging the Image Directory
        self.dirManager(self.img_destination_folder, "replace")
        print("Saving Images at :", self.img_destination_folder)

        #Saving pages in jpeg format
        for i,page in enumerate(pages):
            image_name = "{}/{}__page__{}.png".format(self.img_destination_folder,"fp",i)
            try:
                page.save(image_name, 'png')
                print("{} saved successfully!".format(image_name))
            except Exception as e:
                print("Could not save image: {}\nFollowing error occured: {}".format(image_name, e))

        print("PDF2Image Operation Completed!")

    def detect_images(self):
        # Realizing images in the images directory
        images_list = os.listdir(self.img_destination_folder)

        # Managing Floor Plans output directory
        self.dirManager(self.fp_destination_folder, "replace")

        for i,image in enumerate(images_list):

            print("Processing Image {}/{}: {}".format(i+1, len(images_list), image))

            # image_dir = self.img_destination_folder + "\\" + image
            image_dir = os.path.join(self.img_destination_folder, image)
            print("Image at:", image_dir)

            # Read in the image
            read_image = io.imread(image_dir)

            # Process it to neural network specs
            processed, rescale_factor, rotated = preprocess(read_image)

            # Pass it through the model
            mask = model.predict(processed.reshape(1, *processed.shape))

            # Postprocess the mask
            bounding_box = postprocess(read_image, mask, rescale_factor, rotated)

            # If a floor plan is found, write it to disk as a PNG
            if bounding_box is not None:
                # Formulate filepath
                filepath = os.path.join(self.fp_destination_folder, image)
                
                print("-> Floor Plan found ! Writing at {}".format(filepath))

                # in_hsv_h = color.convert_colorspace(in_hsv_h, 'HSV', 'RGB')
                
                # dtype before: float64
                # print('dtype before:', bounding_box.dtype)
                # ------------------------------------------
                # dtype after:  uint8
                # bounding_box=img_as_ubyte(bounding_box)
                # print('dtype: after', bounding_box.dtype)
                
                # Show data type of image
                print('dtype:', bounding_box.dtype)

                io.imsave(filepath, bounding_box)
            
            # Otherwise, keep calm and carry on
            else:
                print("-> No Floor Plan found; continuing.")

            print()  # for print indentation

        print("All Floor Plans Extracted Successfully!")
        
    def prompt_user(self):
        inbac.main(self.fp_destination_folder)


if __name__ == '__main__':
    agent = PDF_to_Floor_Plans('fp.pdf', 300, 'PDF_Images', 'Model_Images')
    # agent.pdf2images()
    # agent.detect_images()
    agent.prompt_user()