import logging

from gensim.models import LdaModel
from gensim import corpora
import nltk
from nltk.stem.wordnet import WordNetLemmatizer

import os
import time

from pymongo import MongoClient
import nltk

from settings import Settings

from itertools import izip
import numpy as np
import scipy as sp

def get_base(unit ='bit'):
    if unit == 'bit':
        log = sp.log2
    elif unit == 'nat':
        log = sp.log 
    elif unit in ('digit', 'dit'):
        log = sp.log10  
    else:
        raise ValueError('The "unit" "%s" not understood' % unit)
    return log

def shannon_entropy(freq, unit='bit'):
    """Calculates the Shannon Entropy (H) of a frequency.
    
    Arguments:
    
        - freq (``numpy.ndarray``) A ``Freq`` instance or ``numpy.ndarray`` with 
          frequency vectors along the last axis.
        - unit (``str``) The unit of the returned entropy one of 'bit', 'digit' 
          or 'nat'.
    """
    log = get_base(unit)
    shape = freq.shape # keep shape to return in right shape
    Hs = np.ndarray(freq.size / shape[-1]) # place to keep entropies
    # this returns an array of vectors or just a vector of frequencies
    freq = freq.reshape((-1, shape[-1])) 
    # this makes sure we have an array of vectors of frequencies
    freq = np.atleast_2d(freq)
    # get fancy indexing
    positives = freq != 0.
    for i, (freq, idx) in enumerate(izip(freq, positives)):
        freq = freq[idx] # keep only non-zero
        logs = log(freq) # logarithms of non-zero frequencies
        Hs[i] = -np.sum(freq * logs)
    Hs.reshape(shape[:-1])
    return Hs

def jensen_shannon_divergence(freq, weights =None, unit='bit'):
    """
    Calculates the Jensen-Shannon Divergence (Djs) of two or more frequencies.
    The weights are for the relative contribution of each frequency vector. 
    
    Arguments:
    
        - freq (``numpy.ndarray``) A ``Prof`` instance or a rank-2 array of 
          frequencies along the last dimension.
        - weights (``numpy.ndarray``) An array with a weight for each 
          frequency vector. Rank-1.
        - unit (``str``) see: the function ``shannon_entropy``.
    """
    if weights is not None:
        if len(freq) != len(weights):
            raise ValueError('The number of frequencies and weights do not match.')
        if (freq.ndim != 2) or (len(freq) < 2):
            raise ValueError('At least two frequencies in a rank-2 array expected.')
    weighted_average = np.average(freq, axis=0, weights=weights)
    H_avg_freq = shannon_entropy(weighted_average, unit)
    H_freq = shannon_entropy(freq, unit)
    avg_H_freq = np.average(H_freq, weights=weights)
    JSD = H_avg_freq - avg_H_freq
    return JSD

class Predict():
    def __init__(self):
        dictionary_path = "dictionary.dict"
        lda_model_path = "lda_model_50_topics.lda"
        self.dictionary = corpora.Dictionary.load(dictionary_path)
        self.lda = LdaModel.load(lda_model_path)

    def load_stopwords(self):
        stopwords = {}
        with open('stopwords.txt', 'rU') as f:
            for line in f:
                stopwords[line.strip()] = 1

        return stopwords

    def extract_lemmatized_nouns(self, new_review):
        stopwords = self.load_stopwords()
        words = []

        sentences = nltk.sent_tokenize(new_review.lower())
        for sentence in sentences:
            tokens = nltk.word_tokenize(sentence)
            text = [word for word in tokens if word not in stopwords]
            tagged_text = nltk.pos_tag(text)

            for word, tag in tagged_text:
                words.append({"word": word, "pos": tag})

        lem = WordNetLemmatizer()
        nouns = []
        for word in words:
            if word["pos"] in ["NN", "NNS"]:
                nouns.append(lem.lemmatize(word["word"]))

        return nouns

    def run(self, new_review):
        nouns = self.extract_lemmatized_nouns(new_review)
        new_review_bow = self.dictionary.doc2bow(nouns)
        new_review_lda = self.lda[new_review_bow]

        #print new_review_lda
        return new_review_lda

def extract_distribution(topic_dist):
    dist = []
    for i in range(len(topic_dist)):
        dist.append(topic_dist[i][1])
    return dist

def main():
    #logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

    # new_review = "It's like eating with a big Italian family. " \
    #              "Great, authentic Italian food, good advice when asked, and terrific service. " \
    #              "With a party of 9, last minute on a Saturday night, we were sat within 15 minutes. " \
    #              "The owner chatted with our kids, and made us feel at home. " \
    #              "They have meat-filled raviolis, which I can never find. " \
    #              "The Fettuccine Alfredo was delicious. We had just about every dessert on the menu. " \
    #              "The tiramisu had only a hint of coffee, the cannoli was not overly sweet, " \
    #              "and they had this custard with wine that was so strangely good. " \
    #              "It was an overall great experience!"


    reviews_collection = MongoClient(Settings.MONGO_CONNECTION_STRING)[Settings.REVIEWS_DATABASE][
        Settings.REVIEWS_COLLECTION]

    reviews_cursor = reviews_collection.find()
    reviewsCount = reviews_cursor.count()
    reviews_cursor.batch_size(1000)

    test_rst_collection = MongoClient(Settings.MONGO_CONNECTION_STRING)[Settings.REVIEWS_DATABASE][
        "test_result"]


    # done = 0
    # start = time.time()
    # values = np.array([[0.3, 0.3, 0.4], [0.3, 0.4, 0.3]])
    # print jensen_shannon_divergence(values, weights =None, unit='bit')

    for review in reviews_cursor:
        new_review = review["text"]
        predict = Predict()
        review_topic = extract_distribution(predict.run(new_review))
        sentences = nltk.sent_tokenize(new_review)
        sentencesCount = 0
        for sentence in sentences:
            predict = Predict()
            sent_topic = extract_distribution(predict.run(sentence))
            if(len(review_topic) == len(sent_topic)):
                values = np.array([review_topic, sent_topic])
                diff = jensen_shannon_divergence(values, weights =None, unit='bit')
                test_rst_collection.insert({
                    "reviewId": review["reviewId"],
                    "sentencesId": sentencesCount,
                    "tip": True if diff < 0.3 else False
                })

            sentencesCount = sentencesCount + 1


        # done += 1
        # if done % 100 == 0:
        #     end = time.time()
        #     os.system('clear')
        #     print 'Done ' + str(done) + ' out of ' + str(reviewsCount) + ' in ' + str((end - start))


if __name__ == '__main__':
    main()


