import numpy as np
import math
from collections import defaultdict
import numpy.linalg as la
import collections
import re
from nltk.stem import PorterStemmer
from nltk.corpus import stopwords


def search_tf_idf(query,t_lines):

    query = build_terms(query)
    docs = set()

    index, tf, df, idf, title_index = create_inverted_index(t_lines)

    term_docs = []
    for term in query:
        try:
            # store in term_docs the ids of the docs that contain "term"
            term_docs = [posting[0] for posting in index.get(term.lower(), [])]
            
            # docs = docs Intersaction term_docs
            if len(docs) == 0:
              docs = set(term_docs)
            else:
              docs.intersaction(set(term_docs))
        except:
            #term is not in index
            pass

    docs = list(docs)
    ranked_docs, result_scores = rank_documents(query, docs, index, idf, tf)

    return ranked_docs, result_scores


def rank_documents(terms, docs, index, idf, tf):

    doc_vectors = defaultdict(lambda: [0] * len(terms)) # I call doc_vectors[k] for a nonexistent key k, the key-value pair (k,[0]*len(terms)) will be automatically added to the dictionary
    query_vector = [0] * len(terms)

    # compute the norm for the query tf
    query_terms_count = collections.Counter(terms)  # get the frequency of each term in the query.

    query_norm = la.norm(list(query_terms_count.values()))

    for termIndex, term in enumerate(terms):  #termIndex is the index of the term in the query
        if term not in index:
            continue

        # Compute tf*idf(normalize TF as done with documents)
        query_vector[termIndex]=(query_terms_count[term]/query_norm) * idf[term]

        # Generate doc_vectors for matching docs
        for doc_index, (doc, postings) in enumerate(index[term]):

            if doc in docs:
                doc_vectors[doc][termIndex] = tf[term][doc_index] * idf[term]  # TODO: check if multiply for idf

    doc_scores=[[np.dot(curDocVec, query_vector), doc] for doc, curDocVec in doc_vectors.items() ]
    doc_scores.sort(reverse=True)
    result_docs = [x[1] for x in doc_scores]
    result_scores = [x[0] for x in doc_scores]

    if len(result_docs) == 0:
        print("No results found, try again")

    return result_docs, result_scores


def create_inverted_index(lines):
    index = defaultdict(list)
    tf = defaultdict(list)          #term frequencies of terms in documents (documents in the same order as in the main index)
    df = defaultdict(int)           #document frequencies of terms in the corpus
    title_index = defaultdict(str)
    idf = defaultdict(float)

    num_tweets = len(lines)
    tweet_index = {}

    for line in lines:          #for each tweet in lines
        line_arr = line.split("|")
        tweet = line_arr[0]
        terms = ''.join(line_arr[1:])
        terms = build_terms(terms)
        title = line_arr[1]
        title_index[tweet] = title

        current_page_index = {}

        # Compute the denominator to normalize term frequencies, norm is the same for all terms of a document
        norm = 0
        for position, term in enumerate(terms):
            current_page_index.setdefault(term, [tweet, []])[1].append(position)
            norm += 1

        norm = math.sqrt(norm)

        # calculate the tf(dividing the term frequency by the above computed norm) and df weights
        for term, posting in current_page_index.items():
            # append the tf for current term (tf = term frequency in current doc/norm)
            tf[term].append(round(len(posting[1]) / norm, 4))
            # increment the document frequency of current term (number of documents containing the current term)
            df[term] += 1

        # merge the current page index with the main index
        for term_page, posting_page in current_page_index.items():
            index[term_page].append(posting_page)

    # Compute IDF following the formula (3) above. HINT: use np.log 
    for term in df:
        idf[term] = round(math.log(num_tweets / df[term]), 4)

    return index, tf, df, idf, tweet_index


def build_terms(text):

    stemmer = PorterStemmer()
    stop_words = set(stopwords.words('english'))
    text = text.lower()
    text = re.sub('http[s]?://\S+', '', text)            # Bonus: Remove urls
    text = re.sub('[\W_]+', ' ', text)                   # Bonus: Remove emojis, symbols...
    text = text.split()                                  # Tokenize the text to get a list of terms
    text = [x for x in text if x not in stop_words]      # Eliminate the stopwords
    text = [stemmer.stem(word) for word in text]         # Perform stemming

    return text