from kivy.properties import StringProperty
from utils.xcamera import XCamera
from kivy.uix.popup import Popup
from utils.image import Image
from kivy.lang import Builder
from kivy.clock import Clock
from kivy.app import App

Builder.load_file("reader.kv")


class MyPopup(Popup):
    result = StringProperty()
    type = StringProperty()

    def __init__(self, result, type, *args, **kwargs):
        """
        Popup constructor.
        :param result: string of text be shown inside of a popup.
        :param type: string of a qr type, it's shown as popup title
        :param args: None
        :param kwargs: None
        """
        super().__init__(*args, **kwargs)
        self.result = result
        self.type = type

    def show_popup(self):
        """
        Shows popup object and takes care of showing only one popup at a time.
        :return: None
        """
        # Check if any instance of popup is currently active
        # if there is any more than 1 popup do not show new one
        if len(App.get_running_app().root_window.children) <= 1:
            self.open()


class QReader(XCamera):
    def __init__(self, *args, **kwargs):
        """
        QReader constructor which is responsible for qr recognition.
        :param args: None
        :param kwargs: None
        """
        self.start()
        self.result = StringProperty()
        self.type = StringProperty()
        self.app = App.get_running_app()
        super().__init__(*args, **kwargs)

    def start(self):
        """
        Function to trigger callback function every half of a second to detect QR codes,
        has to be invoked in constructor object and it's life depends on life of an QReader object.
        :return: None
        """
        Clock.schedule_interval(self.change_state, 0.5)  # call check_callback every half a second

    def change_state(self, callback_arg):
        """
        Detects every half of a second if QR recognition occurred, if it did then popup is shown.
        This function is triggered every half of a second and changes rectangle color to green, when
        QR code is detected
        :param callback_arg: None
        :return: None
        """
        if self.get_camera_texture() is None:
            return

        upper_left, lower_right = self.get_rectangle_angles()

        image_to_obtain = Image(texture=self.get_camera_texture(),
                                upper_left_corner=upper_left,
                                lower_right_corner=lower_right)

        opencv_img = image_to_obtain.convert_kivy_image_to_opencv_image(self.get_camera_texture())
        image_to_obtain.image = opencv_img

        image_to_obtain.process_image()

        state, self.result, self.type = image_to_obtain.decode_image(image_to_obtain.image)

        if state is True:
            self.current_state = "found"
            popup = MyPopup(self.result, self.type)
            popup.show_popup()
        else:
            self.current_state = "not_found"
            self.get_camera_texture()
