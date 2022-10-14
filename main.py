"""
This file is the main program
Contents:
    imports
    Class TheGame:
        Static Variables
        Constructor
    Class TheFlagApp
    Main Running line
"""


from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.widget import Widget
from kivy.core.window import Window
from kivy.properties import StringProperty, ColorProperty, NumericProperty, BooleanProperty, Clock
from timer import Timer
import logging
from kivy.utils import platform

# If the platform is desktop, then use desktop dimensions
if platform not in ['android', 'ios']:
    Window.size = (840, 1163)


# The main class, inherits BoxLayout class
class TheGame(BoxLayout):

    # Some constants, never changed
    BACKGROUND_COLOR = 4/256, 59/256, 92/256, 1     # Blue degree
    TIME_BETWEEN = 2       # Time between result of the previous question and the next one
    FPS = 10        # Number of frames per second

    # Some variables will change during the game
    FLAG_SRC = StringProperty('./Flags/')     # Flag's image source
    timer = Timer()     # Timer object

    # Texts on the four buttons
    b1_text = StringProperty('')
    b2_text = StringProperty('')
    b3_text = StringProperty('')
    b4_text = StringProperty('')

    # Colors of the four buttons
    b1_color = ColorProperty(BACKGROUND_COLOR)
    b2_color = ColorProperty(BACKGROUND_COLOR)
    b3_color = ColorProperty(BACKGROUND_COLOR)
    b4_color = ColorProperty(BACKGROUND_COLOR)

    # Font sizes of the four buttons
    b1_size = NumericProperty(42)
    b2_size = NumericProperty(42)
    b3_size = NumericProperty(42)
    b4_size = NumericProperty(42)

    # Texts and colors for score & time bar
    score_text = StringProperty('')
    timer_text = StringProperty('')
    score_color = ColorProperty(BACKGROUND_COLOR)
    image_color = ColorProperty(BACKGROUND_COLOR)

    # Disability of slider (Not Enability)
    slider_disability = BooleanProperty(False)

    # Button will work as Start or End game
    start_end_switch = StringProperty('Start Game')

    TOTAL_NUMBER = NumericProperty(20)       # Total number of questions
    CURRENT_QUESTION = 1    # Index of the current questions (starts from 1)
    USER_SCORE = 0          # Number of correctly-answered questions (so far)
    FRAME_COUNTER = 0       # Index of the current frame (restarted every second)
    countries = []          # Here the list of countries will be copied

    RIGHT_ANSWER_N = 0      # Index of the button that carries the right answer
    NEXT_QUESTION_FLAG = False      # Alarm to check if we've to move to next question
    START_GAME_FLAG = False         # Alarm to check if we've to start new game
    END_GAME_FLAG = False           # Alarm to check if we've to end the game
    HALT = True     # Is the game on halt now?

    # Importing methods from game_core
    from game_core import start_or_end, start_game, end_game, next_question
    from game_core import check_answer, on_slider
    from game_core import update_score_bar, update_timer_bar, update

    # Constructor
    def __init__(self, **kwargs):
        # Constructing BoxLayout class
        super().__init__(**kwargs)

        # Creating schedule update to be called every 1/FPS second
        Clock.schedule_interval(self.update, 1/self.FPS)



# The class of the app that is written in the kivy file
class TheFlagApp(App):
    pass


# MAIN
# Running the whole thing
TheFlagApp().run()
