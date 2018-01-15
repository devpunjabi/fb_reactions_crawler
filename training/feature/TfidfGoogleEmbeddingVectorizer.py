import numpy as np
from training.feature.GoogleEmbeddingFeature import GoogleEmbeddingFeature
from sklearn.feature_extraction.text import TfidfVectorizer
from collections import defaultdict


class TfidfGoogleEmbeddingVectorizer(GoogleEmbeddingFeature):

    def fit(self, X, y):
        tfidf = TfidfVectorizer(analyzer=lambda x: x)
        tfidf.fit(X)
        # if a word was never seen - it must be at least as infrequent
        # as any of the known words - so the default idf is the max of
        # known idf's
        max_idf = max(tfidf.idf_)
        self.word2weight = defaultdict(
            lambda: max_idf,
            [(w, tfidf.idf_[i]) for w, i in tfidf.vocabulary_.items()])

        return self

    def transform(self, X):
        return np.array([
                np.mean([self.word2vec[w] * self.word2weight[w]
                         for w in self.tokenize_doc(words) if w in self.word2vec] or
                        [np.zeros(self.dim)], axis=0)
                for words in X
            ])