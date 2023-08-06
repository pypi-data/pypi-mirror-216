__version__ = '0.1.1'

import random as rd

class bottle:
  def __init__(self, string):
    self.__string = str(string)
  
  def refract(self):
    list = [
      self.__string[
        rd.randint(0, len(self.__string)):rd.randint(0, len(self.__string))
      ] for i in range(len(self.__string))
    ]
    
    return(list)

  def sink(self):
    character = ''

    for char in range(len(self.__string)):
      string = self.__string + 'e'
      character += str(ord(string[char]) + ord(string[char + 1]))

    return(character)

  def clone(self):
    return(bottle(self.__string))