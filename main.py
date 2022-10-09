"""
This file is the main program
Contents:
    imports
    Class BoxLayoutExample:
        Static Variables
        Constructor
        Functions:
            start_game
            end_game
            next_question
            check_answer
            update_score_bar
            update_timer_bar
            update
    Class TheFlagApp
    Main Running line
"""


from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.widget import Widget
from kivy.core.window import Window
from kivy.properties import StringProperty, ColorProperty, NumericProperty, BooleanProperty, Clock
from flags import ALL_THE_COUNTRIES
from random import shuffle, randint
from time import sleep
from timer import Timer
import logging
from kivy.utils import platform

# If the platform is desktop, then use desktop dimensions
if platform not in ['android', 'ios']:
    Window.size = (840, 1163)


# The main class, inherits BoxLayout class
class BoxLayoutExample(BoxLayout):

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
    b1_size = NumericProperty(15)
    b2_size = NumericProperty(15)
    b3_size = NumericProperty(15)
    b4_size = NumericProperty(15)

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
    countries = []

    RIGHT_ANSWER_N = 0      # Index of the button that carries the right answer
    NEXT_QUESTION_FLAG = False      # Alarm to check if we've to move to next question
    START_GAME_FLAG = False         # Alarm to check if we've to start new game
    END_GAME_FLAG = False           # Alarm to check if we've to end the game
    HALT = True     # Is the game on halt now?

    # Constructor
    def __init__(self, **kwargs):
        # Constructing BoxLayout class
        super().__init__(**kwargs)

        # Creating schedule update to be called every 1/FPS second
        Clock.schedule_interval(self.update, 1/self.FPS)


    def start_or_end(self):
        """
        Arguments: only the self object
        Return: None
        Who call it: START/END button
        When will be called: when START/END button is pressed
        Functionality: Calling start_game or end_game
        """
        # If the game is already ended, then call start_game
        if self.HALT:
            self.start_game()

        # If the game is on play, then call end_game
        else:
            self.end_game()

    def start_game(self):
        """
        Arguments: only the self object
        Return: None
        Who call it: start_or_end function
        When will be called: when the user presses START button
        functionality: Preparing all the environment for a new game
        """
        self.countries = ALL_THE_COUNTRIES.copy() # Copying all the countries
        self.HALT = False       # Once this function is called, the game is not in halt anymore
        self.slider_disability = True   # Slider is disable now
        self.start_end_switch = 'End Game'     # Button will work as End Game now
        self.image_color = 'white'      # Image color is white means the image will appear briefly (not actual white)
        self.CURRENT_QUESTION = 1       # First question
        self.USER_SCORE = 0             # Initial score
        self.update_score_bar()     # Updating the score bar with the initial score (zero)
        self.FRAME_COUNTER = 0      # Clearing the frames counter
        self.timer.reset()          # Resetting the timer
        self.update_timer_bar()     # Updating the timer bar with the new timer (00:00)
        self.START_GAME_FLAG = True     # Setting the start game alarm
        self.NEXT_QUESTION_FLAG = True  # Setting the next question alarm


    def end_game(self):
        """
        Arguments: only the self object
        Return: None
        Who call it: the schedule update function and start_or_end function
        When will be called: when the END_GAME_FLAG is true, or when the user presses END button
        Functionality: Stopping every thing from work
        """
        self.HALT = True    # The game is on halt now
        self.slider_disability = False      # Slider is enable now
        self.start_end_switch = 'Start Game'       # Button will work as Start Game now
        self.image_color = self.BACKGROUND_COLOR       # That makes the (empty) image appears in the same color as the rest of the components
        self.update_score_bar()     # Updating score bar with the final score
        self.FLAG_SRC = './Flags/'    # Removing the flag image
        # Removing all texts from the four buttons and resetting their colors
        for i in range(1,5):
            setattr(self, f'b{i}_text', '')
            setattr(self, f'b{i}_color', self.BACKGROUND_COLOR)
        self.END_GAME_FLAG = False      # To avoid calling it once more


    def on_slider(self, widget):
        """
        Arguments: the self object and the slider widget
        Return: None
        Who call it: the slider widget
        When will be called: when the slider is slided
        Functionality: Changing the total number of questions
        """
        # Casting the slider value always into integer
        self.TOTAL_NUMBER = int(widget.value)



    def next_question(self):
        """
        Arguments: only the self object
        Return: None
        Who call it: the schedule update function
        When will be called: when the NEXT_QUESTION_FLAG is true
        Functionality: Creating and displaying the question
        """
        self.update_score_bar()     # Updating score bar based upon the latest result
        # Resetting all colors of the four buttons
        for i in range(1,5):
            setattr(self, f'b{i}_color', self.BACKGROUND_COLOR)

        # Now it's time for the algorithm of creating the question
        del self.countries[-1]       # Deleting the previuos right country
        shuffle(self.countries)      # Randomly shuffling the list of countries
        right_country = self.countries[-1]   # Last country is chosen to be the right country
        wrong_countries = self.countries[:4] # First 4 countries are chosen to be the wrong choices
        # You may ask why we choose 4 wrong countries when we only need 3 + the right one
        # Well, one of them will be replaced by the right country, this makes getting
        # the index of the right answer much easier

        self.FLAG_SRC = './Flags/'+right_country.flag_src     # Displaying the flag of the right country
        self.RIGHT_ANSWER_N = randint(1, 4)     # Creating random number from 1 to 4
        wrong_names = [country.name for country in wrong_countries] # Getting the names of the four wrong countries
        wrong_sizes = [country.font_size for country in wrong_countries] # Getting the corresponding font sizes of the four wrong countries
        wrong_names[self.RIGHT_ANSWER_N - 1] = right_country.name   # Replacing the randomly chosen wrong country with the right one
        wrong_sizes[self.RIGHT_ANSWER_N - 1] = right_country.font_size # Replacing with the right font size

        # Displaying names of the choices
        for i in range(1,5):
            setattr(self, f'b{i}_text', wrong_names[i-1])
            setattr(self, f'b{i}_size', wrong_sizes[i-1])

        print(f'{self.b1_size} {self.b2_size} {self.b3_size} {self.b4_size}')


    def check_answer(self, btn):
        """
        Arguments: the object and the pressed button index (number from 1 to 4)
        Return: None
        Who call it: any one of the four choices buttons
        When will be called: when a button of those four is pressed
        Functionality: Checking if the pressed answer is right then checking if the whole game is done
        """
        # If the game is on halt then no press should make a difference
        if self.HALT:
            return

        # If it's the wrong answer, color it with red!
        if btn != self.RIGHT_ANSWER_N:
            setattr(self, f'b{btn}_color', 'red')

        # If it's the right answer, increse user score
        else:
            self.USER_SCORE += 1

        # In both cases (whatever the answer) the right answer button should be green
        setattr(self, f'b{self.RIGHT_ANSWER_N}_color', 'green')

        # If we haven't just finished the last question...
        if self.CURRENT_QUESTION < self.TOTAL_NUMBER:
            self.CURRENT_QUESTION += 1      # ...increase the current question index
            self.NEXT_QUESTION_FLAG = True  # ...and turn on the NEXT_QUESTION_FLAG

        # If we indeed just finished the last question...
        else:
            self.END_GAME_FLAG = True   # ...turn on the END_GAME_FLAG


    def update_score_bar(self):
        """
        Arguments: only the self object
        Return: None
        Who call it: start_game, end_game & next_question
        When will be called: when score bar is in need to update
        functionality: Updating the text and the color of the score bar
        """
        # Changing the text
        self.score_text = f'Question:{self.CURRENT_QUESTION}/{self.TOTAL_NUMBER}              Score:{self.USER_SCORE}'

        # Calculating the % of the user score
        try:
            score_ratio = self.USER_SCORE / (self.CURRENT_QUESTION-1)
        # If the previous line causes a division-by-zero problem...
        except:
            score_ratio = 0.5   # ...then act like 50%

        # Changing the color (more good more green, more bad more red)
        self.score_color = (1-score_ratio, score_ratio, 0.3 , 1)


    def update_timer_bar(self):
        """
        Arguments: only the self object
        Return: None
        Who call it: start_game and the update schedule function
        When will be called: in the very beginning then when a second passed
        functionality: Updating the text of the timer bar
        """
        # Getting the time in a string form "MM:SS"
        self.timer_text = self.timer.get_str()


    def update(self, dt):
        """
        Arguments: the object and the delta time
        Return: None
        Who call it: Kivy's schduling clock
        When will be called: continiously, every 1/FPS seconds
        Functionality: Observing the current state and taking suitable actions
        """
        # If game is on halt, then this function should do nothing
        if self.HALT:
            return

        # Updating the frames counter (taking mod 10)
        self.FRAME_COUNTER = (self.FRAME_COUNTER + 1) % self.FPS


        # If we started a new second...
        if not self.FRAME_COUNTER:
            self.timer.increase()       # ...increse the timer (by second)
            self.update_timer_bar()     # ...and update the timer bar

        # If the NEXT_QUESTION_FLAG is on...
        if self.NEXT_QUESTION_FLAG:
            self.NEXT_QUESTION_FLAG = False     # ...turn off the NEXT_QUESTION_FLAG first
            # ...check if we're on the beginning of a new game
            # If so...
            if self.START_GAME_FLAG:
                self.START_GAME_FLAG = False    # ...turn off the START_GAME_FLAG

            # If we're not on the beginning...
            else:
                # ...sleep for some time to make sure that the gamer saw the result of the previous question
                sleep(self.TIME_BETWEEN)

            # In both cases (beginning of a new game or just new question)
            # We've to move the next question (it might be the first)
            self.next_question()

        # If the END_GAME_FLAG is on (Not the NEXT_QUESTION_FLAG)...
        elif self.END_GAME_FLAG:
            # ...sleep for some time to make sure that the gamer saw the result of the LAST question
            sleep(self.TIME_BETWEEN)
            self.end_game()     #Then end the game


# The class of the app that is written in the kivy file
class TheFlagApp(App):
    pass


# MAIN
# Running the whole thing
TheFlagApp().run()
