import random
import collections
from nltk import NaiveBayesClassifier as nbc
from nltk.classify.maxent import MaxentClassifier as mec
import nltk.classify
import pickle
import math
from sklearn.svm import LinearSVC
from nltk.classify.scikitlearn import SklearnClassifier


class PerformanceFinder:
    def __init__(self):
        self.train_set_size = 0
        self.test_set_size = 0 
        self.total_size = 0
        self.trainSet = []
        self.testSet = []
        self.featureList = []
            

    def findAccuracy(self, classifier):
        return nltk.classify.accuracy(classifier, self.testSet)


    def findNBPerformance(self):
        self.train_set_size, self.test_set_size, self.trainSet, self.testSet = self.findSet()
        classifier = nbc.train(self.trainSet)
        accuracy = self.findAccuracy(classifier)
        return self.train_set_size, self.test_set_size, accuracy

    def findMEPerformance(self):
        self.train_set_size, self.test_set_size, self.trainSet, self.testSet = self.findSet()
        classifier = mec.train(self.trainSet, algorithm='iis', max_iter=15)
        accuracy = self.findAccuracy(classifier)
        return self.train_set_size, self.test_set_size, accuracy


    def findSVMPerformance(self):
        self.train_set_size, self.test_set_size, self.trainSet, self.testSet = self.findSet()
        classifier = SklearnClassifier(LinearSVC())
        classifier.train(self.trainSet)
        accuracy = self.findAccuracy(classifier)
        return self.train_set_size, self.test_set_size, accuracy


    def findSet(self):
        featuresets = pickle.load(open('data/featureSets.pickle','rb'))
        random.shuffle(featuresets)
        self.total_size = len(featuresets)
        self.train_set_size = math.floor((3/4)*self.total_size)
        self.test_set_size = self.total_size - self.train_set_size
        train_set, test_set = featuresets[self.train_set_size:], featuresets[:self.test_set_size]
        self.featureList = []
        self.trainSet = []
        for line in train_set:
            featureVector = line[0]
            sentiment = line[1]
            self.trainSet.append((dict([(word, True) for word in featureVector]), sentiment))
            self.featureList = self.featureList + featureVector

        self.testSet = []
        for line in test_set:
            featureVector = line[0]
            sentiment = line[1]
            self.testSet.append((dict([(word, (word in self.featureList)) for word in featureVector]), sentiment))
    
    
        return self.train_set_size, self.test_set_size, self.trainSet, self.testSet
a = PerformanceFinder()
classifier_name = input("enter classifier num: ")
if classifier_name == '1':
    train_set_size, test_set_size, accuracy = a.findNBPerformance()
    print("Naive Bayes classifier")
elif classifier_name == '2':
    train_set_size, test_set_size, accuracy = a.findMEPerformance()
    print("MaxEnt classifier")
elif classifier_name == '3':
    train_set_size, test_set_size, accuracy = a.findSVMPerformance()
    print("SVM classifier")
print("train_set_size: ", train_set_size, "\ntest_set_size: ", test_set_size, "\naccuracy: ", accuracy)