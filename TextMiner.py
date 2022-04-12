import nltk
from nltk.probability import FreqDist
from nltk.corpus import wordnet
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import re

"""
Text Processing Methods:
"""
nltk.download("wordnet")
nltk.download("stopwords")
nltk.download('punkt')
stop_words = set(stopwords.words("english"))
lemmatizer = WordNetLemmatizer()



def clean_string(text):

    text = text.lower()  # Set all text to lower string
    text = re.sub(r"http.*?(?=\s)", "", text)  # Remove URL's
    text = re.sub(r"[^A-z\s]", "", text)  # Remove punctuation and numbers
    text = re.sub(" +", " ", text)  # Remove multiple spaces
    # text = re.sub(f"{get name from main}", "get name from main", text) # Add use-case dependent term here??
    text = re.sub("(^| ).( |$)", " ", text)  # remove single letters

    word_tokens = nltk.word_tokenize(text)

    filtered_text = []

    for token in word_tokens:  # Remove stop words
        if token not in stop_words:
            filtered_text.append(token)

    lemmatized_text = []

    for word in filtered_text:  # Group words having the same meaning
        lemmatized_text.append(lemmatizer.lemmatize(word))

    return lemmatized_text