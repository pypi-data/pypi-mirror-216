""" File containing the mobile application for this Bronsoneering App"""

try:
    from kivy.app import App
    from kivy.uix.widget import Widget
    from kivy.graphics import Color, Ellipse, Line
    from kivy.uix.button import Button
except ImportError as err:
    from propeller_design_tools.user_io import PDTError

    raise PDTError(err)


class BronsoneeringMainWin(Widget):
    def on_touch_down(self, touch):
        with self.canvas:
            Color(1, 1, 0)
            d = 30.
            Ellipse(pos=(touch.x - d / 2, touch.y - d / 2), size=(d, d))
            touch.ud['line'] = Line(points=(touch.x, touch.y))

    def on_touch_move(self, touch):
        touch.ud['line'].points += [touch.x, touch.y]


class BronsoneeringApplication(App):
    def build(self):
        widg = Widget()
        self.main_win = BronsoneeringMainWin()
        clear_btn = Button(text='Clear')
        clear_btn.bind(on_release=self.clear_canvas)
        widg.add_widget(self.main_win)
        widg.add_widget(clear_btn)
        return widg

    def clear_canvas(self, obj):
        self.main_win.canvas.clear()


if __name__ == '__main__':
    BronsoneeringApplication().run()
