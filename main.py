#!/usr/bin/python
import csv
import string

def main():
    sen = BasicSentimentAnalysis()
    result = sen.analyse_text("I hate Trump, I'm furious, but I love ice cream.")

    if result.error is None:
        print result.percentages
    else:
        print result.error

       
#### SENTIMENT CLASS ####        
class SentimentResult:
    raw = []
    majority_emotion = []
    percentages = {}
    error = None

    def __init__(self, results):
        self.raw = results

        # majority emotion
        current_highest = 0
        for dictionary in results:
            if int(dictionary["occurences"]) > current_highest:
                current_highest = int(dictionary["occurences"])
        if current_highest > 0:
            for dictionary in results:
                if int(dictionary["occurences"]) == current_highest:
                     self.majority_emotion.append(dictionary["emotion"])
        else:
            self.majority_emotion = ['undetermined']

        # percentages
        total = 0
        for result in results:
            total+=result["occurences"]
        # get percentages for the emotions
        for result in results:
            if (total > 0):
                ## double float cast fixes interesting type bug
                self.percentages[result["emotion"]] = float(float(result["occurences"])/total)
            else:
                self.percentages[result["emotion"]] = 0;


class BasicSentimentAnalysis:
    """Basic test of sentiment analysis"""
    word_dict_filenames = [['negative', 'lists/neg-lex-strip.txt'],
                           ['positive', 'lists/pos-lex-strip.txt'],
                           ['angry', 'lists/angry-lex.txt']];
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
        sen = SentimentResult(skews)
        return sen

        
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
