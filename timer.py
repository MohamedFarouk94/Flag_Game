"""
This file contains the timer algorithm
Contents:
    Class Timer:
        Constructor
        Functions:
            increase
            get_str
"""


# The Timer Class
class Timer:
    # Constructor
    def __init__(self):
        self.min = 0
        self.sec = 0

    def increase(self):
        """
        Arguments: only the timer object
        Return: None
        Who call it: the update schedule function
        When will be calles: when a complete second passed
        Functionality: Adding one second to the timer
        """
        # First case: We're in the second 59
        if self.sec == 59:
            self.sec = 0    # Second counter will be zero
            self.min += 1   # Minutes counter increasing by one

        # Second case: Not the second 59
        else:
            self.sec += 1   # Seconds counter increasing by one


    def reset(self):
        """
        Arguments: only the timer object
        Return: None
        Who call it: start_game function
        When will be called: when start_game function is called
        Functionality: Resetting the timer
        """
        self.sec = 0    # Resetting the seconds counter
        self.min = 0    # Resetting the minutes counter


    def get_str(self):
        """
        Arguments: only the timer object
        Return: string on the form "MM:SS"
        Who call it: update_timer_bar function
        When will be called: when update_timer_bar function is called
        Functionality: Creating the timer string on the form "MM:SS"
        """
        # If the seconds counter screens one digit (< 10) then we'll put a leading zero
        sec_str = str(self.sec) if self.sec > 9 else '0'+str(self.sec)

        # The same with the minutes counter
        min_str = str(self.min) if self.min > 9 else '0'+str(self.min)

        # Creating and returning the string on the form "MM:SS"
        return min_str + ':' + sec_str
