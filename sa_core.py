from snownlp import SnowNLP
from textblob import TextBlob


def sa(t):
    s = SnowNLP(t)
    return s.sentiments


def sa_blob(t):
    b = TextBlob(t)
    return b.sentiment.polarity