from kivy.core.image import Image as CoreImage
from kivy.properties import ObjectProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.lang import Builder
from utils.image import Image
from kivy.app import App
from io import BytesIO
import plyer
import os


Builder.load_file("generator.kv")


class QGenerator(BoxLayout):
    qr_image = ObjectProperty(None)

    def __init__(self, *args, **kwargs):
        self.app = App.get_running_app()
        super().__init__(*args, **kwargs)

    def generate(self):
        """
        Takes string typed in text field and converts it to kivy texture object.
        Due to different types of image, whole preprocess from PIL image to kivy texture
        has to be done manually.
        :return: None
        """
        qr_string = self.ids.stringInput.text
        if len(qr_string) != 0:
            # We will generate only non empty QR images
            pil_image = Image.create_qr_img(qr_string)

            # This gets little tricky here as we need to convert PIL image
            # to kivy texture object in order to show it in canvas.
            # Let's start with making data buffer to which we will save the image data.
            data = BytesIO()
            pil_image.save(data, format='png')
            data.seek(0)
            # Later on convert data to pure array and then make kivy texture out of it.
            im = CoreImage(BytesIO(data.read()), ext='png')
            im.texture.save("final.png")
            self.qr_image = im.texture

    def generate_random(self):
        """
        Generates random kivy texture out of random UUID generator function. The string
        of UUID is shown later in text input.
        :return: None
        """
        # Take random UUID generated from function and do
        # exactly the same as function Generate(). This can be optimized later.
        qr_string = str(Image.generate_uuid())
        self.ids.stringInput.text = qr_string
        if len(qr_string) != 0:
            pil_image = Image.create_qr_img(qr_string)
            data = BytesIO()
            pil_image.save(data, format='png')
            data.seek(0)
            im = CoreImage(BytesIO(data.read()), ext='png')
            self.qr_image = im.texture

    def save(self):
        """
        Save already generated image to current location with iamge name same as the
        text input,
        :return: None
        """
        # If we already have generated image we can save it as png in current directory.
        if len(self.ids.stringInput.text) > 0:
            saved_qr_directory = os.path.abspath(
                os.path.join(os.path.dirname(__file__), "image/")
            )
            # Make directory of "image" if it doesn't exist
            if not os.path.exists(saved_qr_directory):
                os.makedirs(saved_qr_directory)
            self.qr_image.save(saved_qr_directory + "/" + self.ids.stringInput.text + ".png")
            plyer.notification.notify(title="QReader", message="Image saved to: {}".format(
                saved_qr_directory + "/" + self.ids.stringInput.text + ".png")
            )
