"""
PART 1: Data loading and preprocessing.
@author Henrik Forbord

This part clean, tokenize and stem data
"""

import codecs
from gensim import corpora, models, gensim
import string
import random
import requests
from nltk.stem.porter import PorterStemmer
from nltk import tokenize

random.seed(123)

# Task 1.1 - 1.2
def text_to_paragraphs(filename):
    """
    Partition file into separate paragraphs
    :param filename: String
    :return: List[String]
    """
    f = codecs.open(filename, "r", "utf-8")
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
    """
    Remove (filter out) paragraphs containing the word "Gutenberg"
    :param paragrahps: List[String]
    :return: List[String]
    """
    filter_obj = (filter(lambda p: "Gutenberg" not in p, paragraphs))
    return list(filter_obj)

# Task 1.4
def paragraphs_to_words(paragraphs):
    """
    Tokenize paragraphs (split them into words)    
    :param paragrahps: List[String]
    :return: List[String]
    """
    for i, p in enumerate(paragraphs):
        paragraphs[i] = p.split(" ")
    return paragraphs
    
# Task 1.5
def remove_punctation(paragraphs):
    """
    Removes !"#$%&'()*+,-./:;<=>?@[\]^_`{|}~\n\r\t and replace it with empty space
    :param paragrahps: List[String]
    :return: List[String]
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
    """
    Convert everything to lower-case
    :param paragrahps: List[String]
    :return: List[String]
    """
    para_lowered = []
    for p in paragraphs:
        word_lowered = []
        for w in p:
            word_lowered.append(w.lower())
        para_lowered.append(word_lowered)
    return para_lowered

# Task 1.6
def stemWords(paragraphs):
    """
    Use the Porter stemmer algorithm to stem words (suffix stripping)
    :param paragrahps: List[String]
    :return: List[String]
    """
    stemmer = PorterStemmer() # Create a new Porter stemmer
    stemmed_para = []
    for p in paragraphs:
        stemmed_words = []
        for w in p:
            stemmed_words.append(stemmer.stem(w))
        stemmed_para.append(stemmed_words)
    return stemmed_para


"""
PART 2: Dictionary building
@author Regine Ruud

This part filter (remove stopwords) and convert paragraphs into Bags-of-Words
"""

#excample document
document_henrik = ["Human machine interface for lab abc computer applications",
"A survey of user opinion of computer system response time",
"The EPS user interface management system",
"System and human system engineering testing of EPS",
"Relation of user perceived response time to error measurement",
"The generation of random binary unordered trees",
"The intersection graph of paths in trees",
"Graph minors IV Widths of trees and well quasi ordering",
"Graph minors A survey"]

stopwords_url = "https://www.textfixer.com/tutorials/common-english-words.txt"

#festcing the stopwords from the url and returning them in a list
def get_stop_words(url):
    stop_words = requests.get(url, params=None).text
    return stop_words.split(',')

#fetching this.stopwords
stopwords_list = get_stop_words(stopwords_url)

#filtering out the stopwords from the document
def filter_out_stopwords(document_lst, lst):
    new_list = []
    for el in document_lst:
        new = [word for word in el.lower().split() if word not in lst]
        new_list.append(new)
    return new_list

#filtering out this.stopwords
list_without_stop = filter_out_stopwords(document_henrik, stopwords_list)


#creating a dictionary with the words and the wordcount (bag of words/bow)
def word_count_dict(lst):
    dict = gensim.corpora.Dictionary(lst)
    print(dict)
    dict = dict.token2id
    return dict

corpus = word_count_dict(list_without_stop)

print(corpus)


"""
PART 3: Retrieval Models
@author Henrik Forbord

This module convert Bags-of-Words into TF-IDF weights and
then LSI(Latent Semantic Indexing) weights. Nearly all the code for this part were given 
out in the hand-out .pdf.file.
"""

# Task 3.1
tfidf_model = gensim.models.TfidfModel(corpus)

# Task 3.2 
tfidf_corpus = tfidf_model[corpus]

# Task 3.3
matrix_sim = gensim.similarities.MatrixSimilarity(corpus)

# Task 3.4
lsi_model = gensim.models.LsiModel(tfidf_corpus, id2word=dict, num_topics=100)
lsi_corpus = gensim.similarities.MatrixSimilarity(tfidf_corpus)

# Task 3.5
print(lsi_model.show_topics())


"""
PART 4: Querying
@Author: Henrik Forbord and Regine Ruud
@Co-Author: Victor Joergensen (1.5 of the methods)

This part let us query the models built in the previous part and report results
"""

# Task 4.1
def preprocessing(query):
    """
    Apply these transformations: remove punctation, tokenize, stem and convert to
    BOW representation (in a way similar as in PART 1)
    :param query: String
    :return: List[String]
    """
    list = query.split()
    for i in range(len(list)):
        list[i] = stemmer.stem(list[i].strip(string.punctuation).lower())
    return list

query = preprocessing("What is the function of money?")
query = dict.doc2bow(query)

# Task 4.2
query_tfidf = tfidf_model[query]
index = gensim.similarities.MatrixSimilarity(tfidf_corpus)

def report_weights(query_tfidf):
    for pair in query_tfidf:
        weight = pair[1]
        word = dict.get(pair[0])
        print(word, ": ", "%0.2f" % weight)

print(report_weights(query_tfidf))

# Task 4.3
def report_most_relevant_paragraphs(query):
    docs2similarity = enumerate(index[query])
    sorted_docs = sorted(docs2similarity, key=lambda kv: -kv[1])[:3]
    relevant_paragraphs = []
    for pair in sorted_docs:
        relevant_paragraphs.append(pair[0])
    for para in relevant_paragraphs:
        print("[Paragraph: ", para+1, "]", "\n")
        lines = filter_obj[para].splitlines(6)
        filter_lines = ""
        n = 0
        try:
            for i in range(6):
                filter_lines += " " +lines[i].strip("\n\r")
                n= i
        except IndexError:
            filter_lines = ""
            for i in range(n+1):
                filter_lines +=" " +lines[i]

        print(filter_lines, "\n")

# Task 4.4
lsi_query = lsi_model[query_tfidf]
sorted_lsi = (sorted(lsi_query, key=lambda kv: -abs(kv[1]))[:3] )
all_topics = lsi_model.show_topics()
for i in sorted_lsi:
    print("[Topic ", i[0], "]")
    print((all_topics[i[0]][1]))
    