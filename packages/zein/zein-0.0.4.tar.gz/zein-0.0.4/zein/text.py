import pandas as pd
import re
import pkg_resources


class ArabicFilter():
    def __init__(self, path: object = pkg_resources.resource_filename('zein', 'data/data.csv')) -> object:  # default argument
        # instance variable
        self.insulting_words = pd.read_csv(path)

    def censor(self, text: str) -> str:
        # compile a regular expression pattern
        pattern = re.compile('|'.join(self.insulting_words['words']), re.IGNORECASE)

        # replace the matching words with asterisks
        censored = re.sub(pattern, lambda m: '*' * len(m.group()), text)
        return censored

    def is_profane(self, text: str) -> bool:
        # compile a regular expression pattern
        pattern = re.compile('|'.join(self.insulting_words['words']), re.IGNORECASE)

        # check if the text matches the pattern
        match = re.search(pattern, text)

        # return True if there is a match, False otherwise
        return bool(match)

    def find_insulting_words(self, text: str) -> list:
        # create an empty list to store the results
        results = []

        # split the text into words
        words = text.split()

        # loop through the words and their indices
        for index, word in enumerate(words):
            # loop through the insulting words
            for insult in self.insulting_words['words']:
                # create a regular expression pattern with some variations
                # for example, allow optional spaces and punctuation around the word
                pattern = re.compile(r'\s*[.,:;!?]*\s*' + insult + r'\s*[.,:;!?]*\s*', re.IGNORECASE)
                # check if the word matches the pattern
                match = re.search(pattern, word)
                # if there is a match, append a tuple of the word and the index to the results list
                if match:
                    results.append((word, index))
                    # break the inner loop to avoid duplicate matches
                    break

        # return the results list
        return results