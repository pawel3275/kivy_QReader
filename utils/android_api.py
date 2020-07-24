from kivy.logger import Logger

from jnius import JavaException, PythonJavaClass, autoclass, java_method

Camera = autoclass('android.hardware.Camera')
AndroidActivityInfo = autoclass('android.content.pm.ActivityInfo')
AndroidPythonActivity = autoclass('org.kivy.android.PythonActivity')
PORTRAIT = AndroidActivityInfo.SCREEN_ORIENTATION_PORTRAIT
LANDSCAPE = AndroidActivityInfo.SCREEN_ORIENTATION_LANDSCAPE


class ShutterCallback(PythonJavaClass):
    __javainterfaces__ = ('android.hardware.Camera$ShutterCallback', )

    @java_method('()V')
    def onShutter(self):
        # apparently, it is enough to have an empty shutter callback to play
        # the standard shutter sound. If you pass None instead of shutter_cb
        # below, the standard sound doesn't play O_o
        pass


class AutoFocusCallback(PythonJavaClass):
    __javainterfaces__ = ('android.hardware.Camera$AutoFocusCallback', )

    def __init__(self, filename, on_success):
        super(AutoFocusCallback, self).__init__()
        self.filename = filename
        self.on_success = on_success

    @java_method('(ZLandroid/hardware/Camera;)V')
    def onAutoFocus(self, success, camera):
        if success:
            Logger.info('xcamera: autofocus succeeded, taking picture...')
            shutter_cb = ShutterCallback()
            picture_cb = PictureCallback(self.filename, self.on_success)
            camera.takePicture(shutter_cb, None, picture_cb)
        else:
            Logger.info('xcamera: autofocus failed')


def set_orientation(value):
    previous = get_orientation()
    AndroidPythonActivity.mActivity.setRequestedOrientation(value)
    return previous


def get_orientation():
    return AndroidPythonActivity.mActivity.getRequestedOrientation()