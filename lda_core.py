import numpy as np
from gensim import corpora, models
from data_processing import *


class LDAr(object):
    def __init__(self,
                 raw_text: list,
                 stop_words: list,
                 num_topics: int = 30,
                 alpha: float = 0.01,
                 eta: float = 0.01,
                 minimum_probability: float = 0.001,
                 update_every: int = 1,
                 chunksize: int = 100,
                 passes: int = 1):
        """
        :param num_topics: the number of topics, default to 30
        :param alpha:
        :param eta:
        :param minimum_probability:
        :param update_every:
        :param chunksize:
        :param passes:
        :param stop_words: local stop word list
        """
        self.rt = raw_text
        self.lda_model_args = {'num_topics': num_topics,
                               'alpha': alpha,
                               'eta': eta,
                               'minimum_probability': minimum_probability,
                               'update_every': update_every,
                               'chunksize': chunksize,
                               'passes': passes}
        self.stop_words = stop_words
        self.cleaned_text = self.sw_clean()
        self.dictionary = self.build_dictionary()
        self.corpus = self.build_corpus()
        self.corpus_tfidf = self.cal_tfidf()
        self.trained_lda = self.train_lda_model()

    def sw_clean(self) -> list:
        print('...Cleaning stop words from text separately...')
        ct = [del_punc(x) for x in self.rt]
        cleaned_text = [[word for word in t.strip().lower().split() if word not in self.stop_words] for t in ct]
        return cleaned_text

    def build_dictionary(self):
        print('...Building dictionary from cleaned texts...')
        d = corpora.Dictionary(self.cleaned_text)
        return d

    def build_corpus(self):
        print('...Counting and building corpus from cleaned texts...')
        corpus = [self.dictionary.doc2bow(t) for t in self.cleaned_text]
        return corpus

    def cal_tfidf(self):
        print('...Calculating TF-IDF from corpus...')
        corpus_tfidf = models.TfidfModel(self.corpus)[self.corpus]
        return corpus_tfidf

    def train_lda_model(self) -> models.LdaModel:
        print('...Training LDA model...')
        lda = models.LdaModel(self.corpus_tfidf, id2word=self.dictionary, **self.lda_model_args)
        return lda

    def gen_topics(self) -> list:
        doc_topics = self.trained_lda.get_document_topics(self.corpus_tfidf)
        idx = np.arange(len(self.cleaned_text))
        r_topics = [doc_topics[i] for i in idx]
        return r_topics

    def gen_terms(self):
        topic_terms = []
        for i in range(self.lda_model_args['num_topics']):
            t = self.trained_lda.get_topic_terms(topicid=i)
            t = [(self.dictionary[x[0]], x[0], x[1]) for x in t]
            topic_terms.append(t)
        return topic_terms
