from FileOperations import *
from tokenizer import *
from nltk.collocations import *
import nltk
from itertools import product
import urlparse
from sklearn.feature_extraction.text import CountVectorizer

from nltk import corpus
from pattern.en import sentiment
from nltk.corpus import wordnet as wn
import re
import time
class TwitterIrony:
    def __init__(self, tweet_type):
        self.tweet_type = tweet_type
        self.tweets = []
        self.tweet_words = []
        self.tweets_tokenized = []
        self.tweet_labels = []
        self.feature_vect = []


    def read_consolidated_tweets(self):
        self.tweets = FileOperations.convert_to_utf(FileOperations.read_file_json("../data/"+self.tweet_type+".json"))
        
    def clean_data(self):
        self.cleaned_tweets = tokenize_data(self.tweets)

    def create_labels_for_data(self):
        for tweet in self.tweets:
            tweet = tweet.lower()
            if "#irony" in tweet or "#ironic" in tweet:
                self.tweet_labels.append(1)
            else:
                self.tweet_labels.append(0)
        print len(self.tweet_labels)

    def extract_features(self):
        for i in range(0,len(self.tweets)):

            feature_dict = {"quotes":0,"exclam":0}
            feature_dict["quotes"] = self.find_quotes(self.tweets[i])
            feature_dict["exclam"] = self.find_exclamations(self.tweets[i])
            sent_features = self.calc_tweet_sentiment(self.cleaned_tweets[i])
            feature_dict["tweet_sent"] = sent_features["tweet_sentiment"]
            feature_dict["pos_high"] = sent_features["pos_high"]
            feature_dict["neg_high"] = sent_features["neg_high"]
            feature_dict["antonym"],feature_dict["antonym_sim"] = self.extract_wordnet_features(self.cleaned_tweets[i])
            self.feature_vect.append(feature_dict)

    def extract_wordnet_features(self, tokenized_tweet):

        ant_bool = 0
        sim_bool = 0
        synset_dict = {}
        for word in tokenized_tweet:
            synset_dict[word] = wn.synsets(word)

        for word in tokenized_tweet:
            antonyms = []
            word_synset = synset_dict[word]
            for synset in word_synset:
                synset_lemmas = synset.lemmas
                for lemma in synset_lemmas:
                    for ant in lemma.antonyms():
                        antonyms.append(ant)
            for ant in antonyms:
                if ant.name in tokenized_tweet:
                    ant_bool = 1
                for other_word in tokenized_tweet:
                    if other_word != word:
                        for synset in synset_dict[other_word]:
                            if ant.synset.path_similarity(synset) > 0.3:
                                sim_bool = 1
            if ant_bool is 1 and sim_bool is 1:
                return (ant_bool,sim_bool)
        return (ant_bool, sim_bool)

    def find_quotes(self,text):
        matches=re.findall(r'\"(.+?)\"',text)
        matches.extend(re.findall(r'\'(.+?)\'',text))
        # matches is now ['String 1', 'String 2', 'String3']
        return len(matches)

    def find_exclamations(self,text):
        matches=re.findall(r'(!)+',text)
        return len(matches)

    def calc_tweet_sentiment(self, tokenized_tweet):
        tweet_sentiment = 0
        pos_high = 0
        neg_high = 0
        for word in tokenized_tweet:
            sent = sentiment(word)
            tweet_sentiment += sent[0]
            if sent[0] > 0:
                pos_high = max(pos_high, sent[0])
            else:
                neg_high = min(neg_high, sent[0])
        return {"tweet_sentiment":abs(tweet_sentiment),"pos_high": pos_high,"neg_high": abs(neg_high)}


def extract_features(tweet_type):
    ti = TwitterIrony(tweet_type)
    ti.read_consolidated_tweets()
    start = time.clock()
    ti.create_labels_for_data()
    end = time.clock()
    print end - start, "second to create labels"
    start = time.clock()
    ti.clean_data()
    end = time.clock()
    print end - start, "second to clean"
    start = time.clock()
    ti.extract_features()
    end = time.clock()
    print end - start, "second to extract features"
    return (ti.feature_vect, ti.tweet_labels)


def main():
    ironic_vect, ironic_labels = extract_features("ironic")
    nonironic_vect, nonironic_labels = extract_features("nonironic")
    FileOperations.write_to_file_json("../data/feature_vectors_ironic.json",ironic_vect, None)
    FileOperations.write_to_file_json("../data/labels_ironic.json", ironic_labels, None)
    FileOperations.write_to_file_json("../data/feature_vectors_nonironic.json",nonironic_vect, None)
    FileOperations.write_to_file_json("../data/labels_nonironic.json", nonironic_labels, None)


if __name__ == "__main__": main()
