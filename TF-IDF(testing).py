#---
# Here will be a script for TF-IDF function. Also I will connect new dataset for work with music test;
# We start searching for song not only for Name, but for main Text words Plan: before 07/25/2025
#---

import math
from textblob import TextBlob as tb

def tf(word,blob):
    return blob.words.count(word)

def n_containing(word, bloblist):
    return sum(1 for blob in bloblist if word in blob.words)

def idf(word, bloblist):
    return math.log(len(bloblist) / (1 + n_containing(word, bloblist)))

def tfidf(word, blob ,bloblist):
    return tf(word, blob)  * idf(word,bloblist)
