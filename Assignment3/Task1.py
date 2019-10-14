"""
Data loading and preprocessing.
This module clean, tokenize and stem data
"""

import codecs
import random
import string
from nltk import tokenize
from nltk.stem.porter import PorterStemmer

random.seed(123)


# Task 1.1 - 1.2
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

# Task 1.3
def filter_paragraphs(paragraphs):
    """Remove (filter out) paragraphs containing the word "Gutenberg"
    
    Arguments:
        para {[List[String]]}
    
    Returns:
        [List[String]] 
    """
    filter_obj = (filter(lambda p: "Gutenberg" not in p, paragraphs))
    return list(filter_obj)

# Task 1.4
def paragraphs_to_words(paragraphs):
    """Tokenize paragraphs (split them into words)
    
    Arguments:
        paragraphs {[List[String]]} 
    
    Returns:
        [List[String]]
    """
    for i, p in enumerate(paragraphs):
        paragraphs[i] = p.split(" ")
    return paragraphs
    
# Task 1.5
def remove_punctation(paragraphs):
    """[Remove punctation]
    
    Arguments:
        paragraphs {[List[Sting]]}
    
    Returns:
        [List[String]]
    """

    para = []
    for p in paragraphs:
        words = []
        for word in p:
            temp = word.replace(string.punctuation + "\r\n\t", " ")
            templist = temp.split(" ")
            for i in templist:
                words.append(i)
        para.append(words)
    return para

def lower(paragraphs):
    """Convert everything to lower-case
    
    Arguments:
        paragraphs {[List[String]]}
    
    Returns:
        [List[String]]
    """
    para_lowered = []
    for p in paragraphs:
        word_lowered = []
        for w in p:
            word_lowered.append(w.lower())
        para_lowered.append(word_lowered)
    return para_lowered

def get_paragraphs(paragraphs):
    """Gives us the paragraphs?
    
    Arguments:
        paragraphs {[List[String]]} 
    
    Returns:
        [List[String]]
    """
    for i, words in enumerate(paragraphs):
        words = remove_punctation(words)
        paragraphs[i] = words
    return paragraphs

# Task 1.7
def stemWords(paragraphs):
    """Use PorterStemmer to stem words (suffix stripping)
    
    Arguments:
        paragraphs {[List[String]]} 
    
    Returns:
        [List[String]]
    """
    stemmer = PorterStemmer() # Create a new Porter stemmer
    stemmed_para = []
    for p in paragraphs:
        stemmed_words = []
        for w in p:
            stemmed_words.append(stemmer.stem(w))
        stemmed_para.append(stemmed_words)
    return stemmed_para

