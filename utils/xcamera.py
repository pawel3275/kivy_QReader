import os

from kivy.clock import mainthread
from kivy.lang import Builder
from kivy.properties import ObjectProperty
from kivy.resources import resource_add_path
from kivy.uix.camera import Camera
from kivy.utils import platform
from kivy.core.window import Window

ROOT = os.path.dirname(os.path.abspath(__file__))
resource_add_path(ROOT)


def is_android():
    return platform == 'android'


def check_camera_permission():
    """
    Android runtime `CAMERA` permission check.
    """
    if not is_android():
        return True

    from android.permissions import Permission, check_permission

    permission = Permission.CAMERA

    return check_permission(permission)


def check_request_camera_permission(callback=None):
    """
    Android runtime `CAMERA` permission check & request.
    """
    had_permission = check_camera_permission()
    if not had_permission:
        from android.permissions import Permission, request_permissions

        permissions = [Permission.CAMERA]
        request_permissions(permissions, callback)

    return had_permission


class XCamera(Camera):
    directory = ObjectProperty(None)
    _previous_orientation = None
    __events__ = ('on_picture_taken', 'on_camera_ready')

    current_state = ObjectProperty(None)
    swidth = ObjectProperty(None)
    sheight = ObjectProperty(None)
    window_sizes = ObjectProperty(None)

    def __init__(self, **kwargs):
        Builder.load_file(os.path.join(ROOT, "xcamera.kv"))
        super().__init__(**kwargs)
        self.current_state = "not_found"
        self.swidth = Window.size[1]
        self.sheight = Window.size[0]
        self.window_sizes = (self.swidth, self.sheight)

    def _on_index(self, *largs):
        """
        Overrides `kivy.uix.camera.Camera._on_index()` to make sure
        `camera.open()` is not called unless Android `CAMERA` permission is
        granted, refs #5.
        """
        @mainthread
        def on_permissions_callback(permissions, grant_results):
            """
            On camera permission callback calls parent `_on_index()` method.
            """
            if all(grant_results):
                self._on_index_dispatch(*largs)

        if check_request_camera_permission(callback=on_permissions_callback):
            self._on_index_dispatch(*largs)

    def _on_index_dispatch(self, *largs):
        super()._on_index(*largs)
        self.dispatch('on_camera_ready')

    def on_picture_taken(self, filename):
        """
        This event is fired every time a picture has been taken.
        """
        pass

    def on_camera_ready(self):
        """
        Fired when the camera is ready.
        """
        pass

    def change_state(self):
        pass

    def get_camera_texture(self):
        # You can go with texture.save which is camera property
        # in order to save the current camera view if needed
        return self.texture

    def get_rectangle_angles(self):
        # this will return square angles from the screen 250x250 in size
        upper_left = (self.center_x-125, self.center_y-125)
        lower_right = (self.center_x+125, self.center_y+125)
        return upper_left, lower_right

