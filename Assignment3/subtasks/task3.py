"""
Retrieval Models.
This module convert Bags-of-Words into TF-IDF weights and
then LSI(Latent Semantic Indexing) weights.
"""

import gensim

# FOR INFORMATION:
# Løist corpus is created in anoter class that I, as we speak, do not have access to.

# Task 3.1
tfidf_model = gensim.models.TfidfModel(corpus)

# Task 3.2 
tdif_corpus = tfidf_model[corpus]

# Task 3.3
matrix_sim = gensim.similarities.MatrixSimilarity(corpus)

# Task 3.4
lsi_model = gensim.models.LsiModel(tfidf_corpus, id2word=dictonary, num_topics=100)
lsi_corpus = gensim.similarities.MatrixSimilarity(tdif_corpus)

# Task 3.5
print(lsi_model.show_topics())
