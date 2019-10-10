"""
Load and process (clean, tokenize and stem) data
"""

import random; random.seed(123)
import codecs


# Open and load the file using codecs
f = codecs.open("pg3300.txt", "r", "utf-8")

