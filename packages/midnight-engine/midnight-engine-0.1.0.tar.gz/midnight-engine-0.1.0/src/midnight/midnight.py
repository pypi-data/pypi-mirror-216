import json
import pyfiglet

#! This project is enchanced by "Better Comments" extension in VSC.
#* Logging to be added on in v0.2.0.
class Data:
    """Data class for storing and loading JSON files and values.
    """
    def __init__(self):
        self.data = {}

    def memory(self, key:str, value:vars):
        """Prepares data for storage in a JSON file.

        Args:
            key (str): Unique key for data.
            value (vars): Value to be stored in JSON file
        """
        self.data[key] = value

    def store(self, filename: str):
        """Stores memory data into a JSON file.

        Args:
            filename (str:): JSON file to store data into.
        """
        with open(filename, 'w') as file:
            json.dump(self.data, file, indent=4)

    @staticmethod
    def load(filename: str):
        """Loads JSON file into a dictionary with setkeys and values.

        Args:
            filename (str): JSON file.

        Returns:
            Dictionary: Contains all vlaues from JSON file with corresponding keys.
        """
        with open(filename, 'r') as file:
            data = json.load(file)
        return data

class UI:
    #* To be added on in v0.2.0
    """UI class for displaying text, ASCII, and graphics.
    """

    @staticmethod
    def draw(text: str):
        #! BETA FEATURE
        """Convert text into ASCII text.

        Args:
            text (str): Inputted text to be converted to ASCII.

        Returns:
            ASCII (str): Returns ASCII text.
        """
        fig = pyfiglet.Figlet(font='slant')
        return fig.renderText(text)
