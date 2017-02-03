"""
LightriftApp
"""
#from random import random
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
#from kivy.uix.StackLayout import StackLayout
from kivy.properties import StringProperty, NumericProperty, ListProperty
from kivy.graphics import Color, Bezier, Line, Rectangle, Ellipse
from kivy.uix.colorpicker import ColorPicker
from kivy.uix.popup import Popup
from kivy.uix.spinner import Spinner

class StandardButton(Button):
    """
    Class for normal buttons
    """
    pass

class PaintModeButton(Button):
    """
    Class for the paint mode buttons and their behaviors
    """
    mode = StringProperty(None)

class ColorPopup(Popup):
    """
    Popup for the color picker wheel.
    """
    pass

class MyPaint(Widget):
    """
    Widget to house the drawing capabilities of the App
    """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.mode = 'free'
        self.color = [0, 0, 0, 1]
        self.line_size = 1
        self.points = []

    def set_line_size(self, new_size):
        """
        Set the working line width/size of Lightrift. Int
        """
        self.line_size = new_size

    def set_mode(self, new_mode):
        """
        Set the working mode of Lightrift. (lines, curves, erase, etc.) Stored
        as string
        """
        self.mode = new_mode

    def set_color(self, new_color):
        """
        Set the working color of Lightrift. Sequence/list of 4 doubles (RGBA).
        """
        print("new color = " + str(new_color))
        self.color = new_color

    def select_color(self, *args):
        """
        Opens popup window with color picker widget for user to select color.
        Selected color is set to working color of Lightrift.
        """
        color_wheel = ColorPopup().open()

    def on_touch_down(self, touch):
        #If the mouse is over the canvas...
        if self.collide_point(*touch.pos):
            with self.canvas:
                #Use working color
                Color(*self.color, mode='rgba')
                #Drawing straight lines...
                if self.mode == 'straight':
                    touch.ud['bezier'] = Bezier(points=(touch.x, touch.y), \
                                       width=self.line_size, segments=1)
                #Drawing Bezier
                elif self.mode == 'bezier':
                    self.points += (touch.x, touch.y)
#                    touch.ud['bezier'] = Line(bezier=(touch.x, touch.y), \
#                                       width=self.line_size, segments=180)
#                    touch.ud['bezier'] = Bezier(points=(touch.x, touch.y), \
#                                       width=self.line_size, segments=180)
                #Drawing freehand or erase (white freehand)
                elif self.mode == 'erase' or self.mode == 'free':
                    #If erase...
                    if self.mode == 'erase':
                        #use color white, but don't make working color white
                        Color([1, 1, 1, 1], mode='rgba')
                    touch.ud['line'] = Line(points=(touch.x, touch.y), \
                                        width=self.line_size)
                #Drawing rectangles
                elif self.mode == 'rect':
                    touch.ud['rectangle'] = Rectangle(pos=(touch.x,touch.y), \
                                                size=(1, 1))
                #Drawing ellipses; ellipse extends rectangle, code is the same
                elif self.mode == 'ellipse':
                    touch.ud['rectangle'] = Ellipse(pos=(touch.x,touch.y), \
                                                size=(1, 1))

    def on_touch_move(self, touch):
        #If still on the canvas, keep drawing
        if self.collide_point(*touch.pos):
            with self.canvas:
                #Movement for rectangles and ellipses
                if self.mode in ('rect', 'ellipse'):
                    touch.ud['rectangle'].size = \
                    [touch.x-touch.ud['rectangle'].pos[0], \
                    touch.y-touch.ud['rectangle'].pos[1]]
                #Movement for freehand and erase
                elif self.mode == 'free' or self.mode == 'erase':
                    touch.ud['line'].points += [touch.x, touch.y]
                #Movement for bezier and straight lines
                elif self.mode in ('bezier', 'straight'):
                    self.points += (touch.x, touch.y)
    #                touch.ud['bezier'].points += (touch.x, touch.y)
    #                touch.ud['bezier'] = Line(bezier=(touch.x, touch.y))


    def on_touch_up(self, touch):
        #developers check to see what state I'm in
        print("%s, %s, %d"%(self.mode, self.color, self.line_size))

        #Finishing drawing bezier or straight lines
        if self.collide_point(*touch.pos):
            with self.canvas:
                if self.mode in ('bezier', 'straight'):
                    if self.mode == 'bezier':
                        Line(bezier=self.points, width=self.line_size, segments=180)
                    else:
                        print(self.points[:2], self.points[-2:])
                        Line(points=(self.points[0],self.points[1],\
                                    self.points[-2],self.points[-1]),\
                        width=self.line_size)
                    self.points = []

class Parent(BoxLayout):
    """
    Parent class for the app
    """
    #def __init__(self, **kwargs):
#        self.color = def_col
    line_size = NumericProperty()
    color = ListProperty([0, 0, 0, 1])

class LightriftApp(App):
    """
    Application-level class, builds the application
    """
    def build(self):
        """
        Builds the app out of widgets
        """
        #instantiate top level, the structure below is defined in lightrift.kv
        the_app = Parent()

        return the_app


if __name__ == '__main__':
    LightriftApp().run()
    