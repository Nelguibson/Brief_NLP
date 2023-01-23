import nltk
nltk.download("punkt")
from nltk.corpus import stopwords
nltk.download("stopwords")
from nltk.stem import WordNetLemmatizer
lm= WordNetLemmatizer()


def corpuser(comment):
    corpus = []
    for i in range(0, len(comment)):
        words = nltk.word_tokenize(str(comment))
        words = [word for word in words if word.isalnum()]
        WordSet = []
        for word in words:
            if word not in set (stopwords.words("french")):
                WordSet.append(word)
        WordSetLem = []
        for word in WordSet:
            word = WordSetLem.append(lm.lemmatize(word))
        message = ' '.join(WordSetLem)
        corpus.append(message)
    
    return corpus
