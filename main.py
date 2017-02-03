#!/usr/bin/python
import csv
import string

# TO DO
# > 
def main():
    sen = BasicSentimentAnalysis()
    result = sen.analyse_text("I hate trump but love ice cream")

    if result.error is None:
        print result.raw
    else:
        print result.error


        
#### SENTIMENT CLASS ####        
class SentimentResult:
    raw = []
    majority_emotion = []
    error = None

    def __init__(self, results):
        self.raw = results

        current_highest = 0
        for emotion in list(results.keys()):
            if results[emotion] > current_highest:
                current_highest = results[emotion]
        if current_highest > 0:
            for emotion in list(results.keys()):
                if results[emotion] == current_highest:
                    self.majority_emotion.append(emotion)
        else:
            self.majority_emotion = ['neutral']


class BasicSentimentAnalysis:
    """Basic test of sentiment analysis"""
    word_dict_filenames = [['negative', 'neg-lex-strip.txt'],
                           ['positive', 'pos-lex-strip.txt'],
                           ['angry', 'angry-lex.txt']];
    word_dict = {}

    def __init__(self):
        #load in our word dictionaries
        for filedict in self.word_dict_filenames:
            with open(filedict[1], 'rb') as f:
                temparray = f.readlines()
                #strip whitespace too
                temparray = [x.strip() for x in temparray]
                self.word_dict[filedict[0]] = temparray          


    def analyse_text(self,tweet):
        #individual words
        words = tweet.split(' ')
        #remove words
        words = self.remove_noise(words)
        #get skews
        skews = []
        for current_emotion in self.word_dict:
            returnedArray = self.get_skew(self.word_dict[current_emotion], words)
            skews.append({"occurences":len(returnedArray),
                          "emotion":current_emotion,
                          "words":"words are here"})
        #parse final results
        final_results = self.parse_results(skews)
        sen = SentimentResult(final_results)
        return sen


    def parse_results(self, skews):
        res = {}
        total = 0
        for result in skews:
            total+=result["occurences"]
        # get percentages for the emotions
        for result in skews:
            if (total > 0):
                ## double float cast fixes interesting type bug
                res[result["emotion"]] = float(float(result["occurences"])/total)
            else:
                res[result["emotion"]] = 0;

        return res

        
    def get_skew(self, current_emotion, sentance):
        found_words = []
        for catword in current_emotion:
            #every word to analyse
            for word in sentance:
                if word == catword:
                    found_words.append(word)
                else:
                    #check for partial words -- !!! this may be problematic !!!
                    if word.find(catword) != -1:
                        found_words.append(word)

        return found_words
    

    def remove_noise(self,words):
        # loop through all words to remove sensitive ones
        for index, word in enumerate(words):
            #strip case
            word = word.lower()
            #check for hashtags
            if "#" in word: 
                word = word.replace("#","")
            #remove punctation that may have stuck to words
            word = word.translate(None, string.punctuation)
            #set final value
            words[index] = word

        #return clean array 
        return words
 
main()
