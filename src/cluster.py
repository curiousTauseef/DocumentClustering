"""
Read file
"""

from datetime import datetime
import argparse
import random
import concurrent.futures

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
import numpy as np

from src.summary import get_vector

NUM_ARTICLES = 20
LANGUAGES = ["deu", "fra", "eng"]

# global variable oops
tokenised = [None]*NUM_ARTICLES
lang = ""

def identity_tokenizer(text):
    return text


def load_token(article):
    with open('files/{}/article_{}.txt'.format(lang, article), 'r') as f:
        data = f.read()
        tokens = get_vector(text=data)
    return article, tokens


def vectorise_and_cluster(lang=None, num_clusters=None):

    if lang is None:
        lang = random.choice(LANGUAGES)

    time1 = datetime.now()
    with concurrent.futures.ProcessPoolExecutor(4) as executor:
        for i, token in executor.map(load_token, range(NUM_ARTICLES)):
            tokenised[i] = token
    time2 = datetime.now()
    diff = time2 - time1
    print("Time taken: {}s".format(diff.microseconds/1e5))

    # time1 = datetime.now()
    # for i in range(NUM_ARTICLES):
    #     with open('files/{}/article_{}.txt'.format(lang, i), 'r') as f:
    #         data = f.read()
    #         tokens = get_vector(text=data)
    #         tokenised.append(tokens)
    # time2 = datetime.now()
    # diff = time2 - time1
    # print(diff.seconds)
    # 12s

    with open('files/metadata_{}.tsv'.format(lang), 'r') as file:
        titles = [l.strip() for l in file]

    tfidf = TfidfVectorizer(max_df=0.8,  max_features=20000,
                            tokenizer=identity_tokenizer,
                            ngram_range=(1,4),
                            lowercase=False,
                            min_df=0.2,
                            use_idf=True, )

    tfidf_matrix = tfidf.fit_transform(tokenised)

    print(tfidf_matrix)

    print("No. of features: {}".format(len(tfidf.get_feature_names())))

    np.savetxt("files/{}.tsv".format(lang), tfidf_matrix.toarray(), delimiter="\t")

    model = KMeans(n_clusters=num_clusters)
    model.fit(tfidf_matrix)

    print("\nTop terms per cluster:")
    order_centroids = model.cluster_centers_.argsort()[:, ::-1]
    clusters = model.labels_.tolist()
    clusters = np.array(clusters)
    terms = tfidf.get_feature_names()
    for i in range(num_clusters):
        print("Cluster %d:" % i)
        for ind in order_centroids[i, :10]:
            print('   %s' % terms[ind])
        print("found in these documents:")
        docs = np.where(clusters==i)[0]
        docs = list(docs)
        for j, d in enumerate(docs):
            print("   {}) {}".format(j+1, titles[d]))
        print()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Vectorise and cluster documents.')
    parser.add_argument('--lang',
                        type=str,
                        help='Language of article. One of eng, deu, fra. If none chosen, a language will be picked at random.')
    parser.add_argument('--num_clusters',
                        type=int,
                        default=3,
                        help='Number of clusters to show. Defaults to 3.')
    args = parser.parse_args()
    lang = args.lang
    vectorise_and_cluster(lang=args.lang, num_clusters=args.num_clusters)
