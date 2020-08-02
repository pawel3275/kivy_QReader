from kivy.uix.screenmanager import ScreenManager, Screen, SlideTransition
from kivy.properties import ObjectProperty
from kivy.app import App

# Below is debug on windows purpose only
# Uncomment for windows
# Code below helps to debug application on windows as it
# shows more or less phone screen.
# from kivy.core.window import Window
# Window.size = (720, 1280)
# KIVY_METRICS_DENSITY = 2


class SuperScreenClass(Screen):
    initial = 0

    def on_touch_down(self, touch):
        self.initial = touch.x
        super().on_touch_down(touch)

    def on_touch_up(self, touch):
        if touch.x - self.initial > 100:
            self.manager.current = "readerScreen"
            self.manager.transition = SlideTransition(direction="left")

        elif touch.x - self.initial < -100:
            self.manager.current = "generatorScreen"
            self.manager.transition = SlideTransition(direction="right")

        super().on_touch_up(touch)


class ReaderScreen(SuperScreenClass):
    pass


class GeneratorScreen(SuperScreenClass):
    pass


class WindowManager(ScreenManager):
    readerScreen = ObjectProperty(None)
    generatorScreen = ObjectProperty(None)


class QRApp(App):
    def build(self):
        m = WindowManager(transition=SlideTransition())
        return m


if __name__ == "__main__":
    QRApp().run()
