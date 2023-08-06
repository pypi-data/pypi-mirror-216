import numpy as np
import re
from scipy.spatial.distance import cosine

# load a Vietnamese corpus as the dictionary
dictionary = ['nốt', 'ruồi',
              'sẹo', 'chấm',
              'sau', 'lông',
              'mày', 'trái',
              'trên', 'tròn',
              'đuôi', 'phải',
              'mắt', 'đầu',
              'mép', 'cánh', 'mũi', 'dưới']


class Correction(object):
    def __init__(self):
        pass

    def preprocess(self, text):
        list_word = []
        for word in text:
            for w in word.split():
                w = w.lower()
                w = re.sub('<.*?>', '', w).strip()
                w = re.sub('(\s)+', r'\1', w)
                list_word.append(w)
        return list_word

    def word2vec(self, word):
        # create a vector of zeros with the same length as the alphabet
        alphabet = 'abcdefghijklmnopqrstuvwxyz0123456789'
        # alphabet = 'aAàÀảẢãÃáÁạẠăĂằẰẳẲẵẴắẮặẶâÂầẦẩẨẫẪấẤậẬbBcCdDđĐeEèÈẻẺẽẼéÉẹẸêÊềỀểỂễỄếẾệỆfFgGhHiI'
        # 'ìÌỉỈĩĨíÍịỊjJkKlLmMnNoOòÒỏỎõÕóÓọỌôÔồỒổỔỗỖốỐộỘơƠờỜởỞỡỠớỚợỢpPqQrRsStTuUùÙủỦũŨúÚụỤưƯừỪửỬữỮứỨựỰvVwWxXyY'
        # 'ỳỲỷỶỹỸýÝỵỴzZ0123456789!"#$%&''()*+,-./:;<=>?@[\]^_`{|}~'

        vec = np.zeros(len(alphabet))
        # set the value of each dimension to the frequency of the corresponding letter in the word
        for letter in word:
            if letter in alphabet:
                vec[alphabet.index(letter)] += 1
        return vec

    def distance(self, word1, word2):
        return cosine(self.word2vec(word1), self.word2vec(word2))

    def suggest(self, word, threshold=0.2):
        if word in dictionary:
            return word
        else:
            closest = min([(self.distance(word, d), d) for d in dictionary])
            if closest[0] <= threshold:
                return closest[1]
            else:
                return word

    def retrieval(self, list_words):
        preprocessed_word = self.preprocess(list_words)
        suggestions = []
        for token in preprocessed_word:
            suggestions.append(self.suggest(token))
        return suggestions
