import gensim
import requests


#excample document, needs to be connected to task 1
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


#creating a dictionary with the words and the wordcount
def word_count_dict(lst):
    dict = gensim.corpora.Dictionary(lst)
    print(dict)
    dict = dict.token2id
    return dict

dct = word_count_dict(list_without_stop)

print(dct)
