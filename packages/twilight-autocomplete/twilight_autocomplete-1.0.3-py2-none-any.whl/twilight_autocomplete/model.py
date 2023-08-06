from nltk.corpus import reuters
from nltk import ngrams
from collections import defaultdict

import nltk
nltk.download('reuters')
nltk.download('punkt')

def train_model(n):
    model = defaultdict(lambda: defaultdict(int))
    for sentence in reuters.sents():
        sentence = ["<s>"] * (n-1) + sentence + ["</s>"]
        ngram = ngrams(sentence, n)
        for gram in ngram:
            prefix = gram[:-1]
            suffix = gram[-1]
            model[prefix][suffix] += 1
    return model

def predict_next_word(prefix, model):
    possible_suffixes = model[prefix]
    return max(possible_suffixes, key=possible_suffixes.get)

def auto_complete(sentence, model, n):
    sentence = sentence.lower().split()
    if len(sentence) < n - 1:
        return "Not enough words in the sentence to generate a prediction."
    prefix = tuple(sentence[-(n - 1):])
    next_word = predict_next_word(prefix, model)
    return next_word
