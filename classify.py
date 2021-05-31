import re
import string
import json
import pickle
from feature_extract import FeatureFinder
from classifier import Classifier


def classifyIt(tweet):
    f = FeatureFinder()
    c = Classifier()
    processed_tweet = f.processTweet(tweet)
    # print(processed_tweet)
    featureVector = f.getFeatureVector(processed_tweet)
    temp1 = {}
    temp1['sentiment'] = c.classifyNB(featureVector)
    temp2 = {}
    temp2['sentiment'] = c.classifyMaxEnt(featureVector)
    temp3 = {}
    temp3['sentiment'] = c.classifySVM(featureVector)
   # print("NB: ", temp1, "\nMaxEnt: ", temp2, "\nSVM: ", temp3)
    return temp1, temp2, temp3



if __name__ == "__main__":

    tweet = input("enter text you want to classify: ")
    classifyIt(tweet)
    print('success\n')
# end
