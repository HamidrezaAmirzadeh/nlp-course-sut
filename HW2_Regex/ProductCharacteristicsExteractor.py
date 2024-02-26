from hazm import *
import nltk
import random
import tqdm
import re
import codecs
import time
from BooksPropertiesExtractor import BookPropertiesExtrator
from ClothesPropertiesExtrator import CLOTHES_PROPERTIES_EXTRACTOR
from DigitalPropertiesExtractor import DIGITAL_PROPERTIES_EXTRACTOR
#import BookPropertiesExtrator
#import DigitalPropertiesExtrator
class ProductCharacteristicsExteractor:
    def __init__(self,text):
        self.text=text

    def run(self):
  #      GeneralPropertiesExtrator()
        properties={}
        b=BookPropertiesExtrator()

        s=CLOTHES_PROPERTIES_EXTRACTOR(self.text)
        Digital=DIGITAL_PROPERTIES_EXTRACTOR(self.text)
        properties.update(Digital.run())
        properties.update(s.run())
        properties.update(b.run(self.text))
        return properties
 #       DigitalPropertiesExtrator()
 #       BookPropertiesExtrator()
