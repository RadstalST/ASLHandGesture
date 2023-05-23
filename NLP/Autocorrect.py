import nltk
from nltk.corpus import words
from nltk.metrics.distance import (
    edit_distance,
    jaccard_distance,
    )
from nltk.util import ngrams
nltk.download('words')
import pandas



class Autocorrect():

    def __init__(self):
        self.correct_spellings = words.words()
        self.spellings_series = pandas.Series(self.correct_spellings)

    def jaccard(self,entries, gram_number):
        
        outcomes = []
        for entry in entries: #iteratively for loop
            if len(entry) <= gram_number:
                outcomes.append('')
                continue
            spellings = self.spellings_series[self.spellings_series.str.startswith(entry[0])] 
            distances = ((jaccard_distance(set(ngrams(entry, gram_number)),
                                        set(ngrams(word, gram_number))), word)
                        for word in spellings)
            closest = min(distances)
            outcomes.append(closest[1])
        return outcomes

    def JDreco(self, entries=['cormulent', 'incendenece', 'validrate']):
        """finds the closest word based on jaccard distance"""
        return self.jaccard(entries, 3)
    
if __name__ == "__main__":
    autocorrect = Autocorrect()
    the_entry = "suculent"
    entries = [the_entry[:i+1] for i in range(0, len(the_entry))]

    print("original entry: ", the_entry)
    print("sequence of entries: ", entries)
    print("autocorrected entry: ", autocorrect.JDreco(entries)[-1])