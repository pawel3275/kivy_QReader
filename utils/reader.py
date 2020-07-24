from kivy.app import App
from utils.xcamera import XCamera
from kivy.clock import Clock
from kivy.uix.popup import Popup
from kivy.properties import StringProperty

from utils.image import Image


class MyPopup(Popup):
    result = StringProperty()
    type = StringProperty()

    def __init__(self, result, type, *args, **kwargs):
        self.result = result
        self.type = type
        print(result)
        print(type)
        super().__init__(*args, **kwargs)


class QReader(XCamera):
    def __init__(self, *args, **kwargs):
        self.start()
        self.result = StringProperty()
        self.type = StringProperty()
        self.app = App.get_running_app()
        super().__init__(*args, **kwargs)

    def start(self):
        Clock.schedule_interval(self.change_state, 0.5)  # call check_callback every 2 seconds

    @staticmethod
    def show_popup(text1, text2):
        show = MyPopup(text1, text2)
        show.open()

    def change_state(self, callback_arg):
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
            print("State changed to found")
            self.current_state = "found"
            self.show_popup(self.result, self.type)
        else:
            print("State changed to not_found")
            self.current_state = "not_found"
            self.get_camera_texture()
