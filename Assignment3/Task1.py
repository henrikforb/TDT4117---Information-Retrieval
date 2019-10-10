"""
Data loading and preprocessing.
This module clean, tokenize and stem data
"""

import random
import codecs
from nltk import tokenize


random.seed(123)

def text_to_paragraphs(file):
    """Partition file into separate paragraphs
    
    Arguments:
        file {[String]} -- [Textfile]
    
    Returns:
        [List] -- [List of paragraphs]
    """

    f = codecs.open("pg3300.txt", "r", "utf-8")
    # Open, read and decode the file on utf-8-standard

    paragraphs = []
    paragraph = ""

    for line in f:
        paragraph += line
        if line.isspace():
            if line != "":
                paragraphs.append(paragraph)
            paragraph = ""
            continue

    return paragraphs

def filter_paragraphs(para):
    """Remove paragraphs containing the word "Gutenberg"
    
    Arguments:
        para {[List[String]]}
    
    Returns:
        [List[String]] 
    """
    filter_obj = (filter(lambda p: "Gutenberg" not in p, para))
    return list(filter_obj)
    