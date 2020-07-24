from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen, NoTransition
from kivy.properties import ObjectProperty


class SuperClass(Screen):
    initial = 0

    def on_touch_down(self, touch):
        self.initial = touch.x

    def on_touch_up(self, touch):
        if touch.x > self.initial:
            self.manager.current = "readerScreen"
        elif touch.x < self.initial:
            self.manager.current = "generatorScreen"
        else:
            print("No move")


class ReaderScreen(SuperClass):
    pass


class GeneratorScreen(SuperClass):
    pass


class WindowManager(ScreenManager):
    readerScreen = ObjectProperty(None)
    generatorScreen = ObjectProperty(None)


class QReaderApp(App):
    def build(self):
        m = WindowManager(transition=NoTransition())
        return m
        #return QReader()


if __name__ == "__main__":
    QReaderApp().run()
