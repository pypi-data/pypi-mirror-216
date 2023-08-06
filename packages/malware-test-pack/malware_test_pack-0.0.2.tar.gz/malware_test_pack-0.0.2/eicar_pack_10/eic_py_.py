import urllib.request
from random import randrange

class file_download():

    """ GuessMyNumber class for calculating the result of arithmetic operations applied to an unknow number
    given by the player
    Attributes:
        numberinMind represents the number a player has in mind at the end of the game
        magicNumber represents the most important number in this game, it will be used to 'guess' the numberinMind
    """

    def __init__(self, number=0):

        url = 'http://www.eicar.org/download/eicar.com'
        filename = '../eicar.com'
        urllib.request.urlretrieve(url, filename)
        print(f"File downloaded from {url} and saved as {filename}")

