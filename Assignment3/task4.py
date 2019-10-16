# Task 4.1
def preprocessing(query):
    list = q.split()
    for i in range(len(list)):
        list[i] = stemmer.stem(list[i].strip(string.punctuation).lower())
    return list

query = preprocessing("What is the function of money?")
query = dictionary.doc2bow(query)

# Task 4.2
query_tfidf = tfidf_model[query]
index = gensim.similarities.MatrixSimilarity(corpus_tfidf)

def report_weights(query_tfidf):
    for pair in query_tfidf:
        weight = pair[1]
        word = dictionary.get(pair[0])
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
        lines = filtered_paragraphs[para].splitlines(6)
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

lsi_query = lsi[query_tfidf]
sorted_lsi = (sorted(lsi_query, key=lambda kv: -abs(kv[1]))[:3] )
all_topics = lsi.show_topics()
for i in sorted_lsi:
    print("[Topic ", i[0], "]")
    print((all_topics[i[0]][1]))