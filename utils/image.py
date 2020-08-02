import cv2
import uuid
import qrcode
import numpy as np
from pyzbar.pyzbar import decode


class Image:
    width = 0
    height = 0
    channels = 0
    image_path = ""
    image = None

    def __init__(self, img_path=None, texture=None, upper_left_corner=(0, 0), lower_right_corner=(0, 0)):
        self.image_path = img_path
        self.image = texture
        self.upper_left_corner = upper_left_corner
        self.lower_right_corner = lower_right_corner

    def load_image(self):
        """"
        Loads image specified in image path passed to constructor
        """
        if self.image is None:
            print("Overriding image with loaded one.")

        self.image = cv2.imread(self.image_path)

    @staticmethod
    def convert_kivy_image_to_opencv_image(image):
        """
        Takes camera texture from kivy as an input and converts it into
        numpy ndarray.
        :param image: image of type camera.texture.Texture
        :return: image od type ndarray
        """
        height, width = image.height, image.width
        ndarray_image = np.frombuffer(image.pixels, np.uint8)
        ndarray_image = ndarray_image.reshape(height, width, 4)
        return ndarray_image

    def process_image(self):
        """"
        Non obligatory method for subtracting image in the middle of the image
        :return None:
        """
        upper_left_corner = (int(self.image.shape[1] / 2 - 125), int(self.image.shape[0] / 2 - 125))
        lower_right_corner = (int(self.image.shape[1] / 2 + 125), int(self.image.shape[0] / 2 + 125))

        upper_left_x = int(upper_left_corner[0])
        upper_left_y = int(upper_left_corner[1])

        bottom_right_x = int(lower_right_corner[0])
        bottom_right_y = int(lower_right_corner[1])

        cv2.rectangle(self.image, (upper_left_x, upper_left_y), (bottom_right_x, bottom_right_y), (0, 255, 0), 2)
        cv2.imwrite("testing.jpg", self.image)
        self.image = self.image[upper_left_y:bottom_right_y, upper_left_x:bottom_right_x]
        self.image = cv2.cvtColor(self.image, cv2.COLOR_RGBA2GRAY)
        # For testing and verifying final image uncomment below
        # cv2.imwrite("testing.jpg", self.image)

    @staticmethod
    def decode_image(image):
        """"
        Decodes image and prints string to output, returns success when qr
        is successfully decoded
        :param image: image containing qr code to be decoded
        :return: status of True when qr code is decoded successfully or False when not.
        """
        qr_codes = decode(image)
        result_string = ""
        result_type = ""

        for qr in qr_codes:
            # Get qr code location and create rectangle over it
            (x, y, w, h) = qr.rect
            cv2.rectangle(image, (x, y), (x + w, y + h), (0, 0, 255), 2)

            qr_data = qr.data.decode("utf-8")
            qr_type = qr.type

            result_string = qr_data
            result_type = qr_type
            return True, result_string, result_type
        return False, result_string, result_type

    @staticmethod
    def generate_uuid(mode=0):
        """"
        Static method for generating UUID based on mode
        :param mode: mode for host ID and time based (Default is random generated)
        :return: generated UUID as string
        """
        if mode == 1:
            return uuid.uuid1()
        else:
            return uuid.uuid4()

    @staticmethod
    def create_qr_img(message="", box_size=10, border=4, path=""):
        """"
        Static method for generating qr code
        :param message: string which will be coded to QR code
        :param box_size: size of an image box (default 10)
        :param border: border line (default 4)
        :param path: path with filename for QR code image (eg. C:\test.png)
        :return None:
        """
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=box_size,
            border=border,
        )
        qr.add_data(message)
        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="white")
        print(img.size)
        img.save("Pilimage.png")
        return img

    def __del__(self):
        cv2.destroyAllWindows()
