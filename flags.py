"""
This file is responsible of creating all the country objects which contain
country names and flags images sources.
Contents:
    importings (one import)
    Class Country:
        Constructor
    get_font_size function
    collect_flags function
    ALL_THE_COUNTRIES list
"""

import os
from kivy.utils import platform


# The country class
class Country:
    # Constructor
    def __init__(self, id, flag_src):
        self.id = id        # Dummy integer, not used in the current version
        self.flag_src = flag_src        # Path of the flag image

        # Extracting the country name from the image path
        # The file path is the country name + ".png" (the dot is the fourth character from the end)
        # we'll take the name and stop before the dot
        # But in the file paths there're underscores instead of spaces
        # So we'll replace them with spaces
        self.name = flag_src[:-4].replace('_', ' ')

        # Duo to displaying problems, we want the 'long' country names to be divided into 2 lines
        # So if the country name has more than 3 words, we'll plug a 'new line' after the 3rd word
        name_splitted = self.name.split(' ')
        if len(name_splitted) > 3:
            self.name = ' '.join(name_splitted[:3]) + '\n' + ' '.join(name_splitted[3:])

        # Getting a proper font size to display
        self.font_size = get_font_size(self.name, name_splitted)


def get_font_size(name, name_splitted):
    """
    Arguments: name and name_splitted
    Return: font size in integer
    Who call it: the Country constructor
    When will be called: when the country object is created
    Functionality: Calculating a proper font size depending on the country name
    """
    MAX_SIZE = 30 if platform in ['android', 'ios'] else 45     # Considering platform

    if len(name_splitted) <= 3:
        return max(MAX_SIZE - len(name)//2, 15)

    return max(MAX_SIZE - len(' '.join(name_splitted[:3]))//2 , 20)



def collect_flags():
    """
    Arguments: None
    Return: List of all countries (in Country object type)
    Who call it: only the last line of this file
    When will be called: only this time
    Functionality: Creating the list of all the Country objects
    """
    ALL_THE_COUNTRIES = []      # Initiating an empty list
    # Iterating over all the images
    for i, flag in enumerate(os.listdir('Flags/')):
        ALL_THE_COUNTRIES.append(Country(i+1, flag))    # Constructing objects

    # Printing number of countries for tracing. Comment if not needed
    # print(f'Number of all countries: {len(ALL_THE_COUNTRIES)}')

    # Returning the list
    return ALL_THE_COUNTRIES


# The list variable ALL_THE_COUNTRIES is the only name from this file to be
# imported in the main file
ALL_THE_COUNTRIES = collect_flags()
