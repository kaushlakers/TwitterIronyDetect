import json
import numpy as np
from nltk.classify.scikitlearn import SklearnClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.naive_bayes import *
from sklearn.metrics import classification_report
from sklearn.metrics import confusion_matrix
from sklearn.svm import LinearSVC
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.tree import DecisionTreeClassifier
from FileOperations import *
import sys
FEATURE_MAP = {"ANT":["antonym","antonym_sim"],"PUNCT":["quotes","exclam"], "SENT":["tweet_sent","pos_high","neg_high"]}
FEATURES = ["antonym","antonym_sim","quotes","exclam","tweet_sent","pos_high","neg_high"]
TRAIN_TEST_SPLIT = 0.75
class IronyClassifier:

    def __init__(self, features):
        self.features = features
        self.X = []
        self.Y = []

    def set_data(self, feature_ironic, labels_ironic, feature_nonironic, labels_nonironic):
        self.feature_vectors_nonironic = feature_nonironic
        self.labels_nonironic = labels_nonironic
        self.feature_vectors_ironic = feature_ironic
        self.labels_ironic = labels_ironic

    def load_data(self):
        self.feature_vectors_nonironic = FileOperations.convert_to_utf(FileOperations.read_file_json("../data/feature_vectors_nonironic.json"))
        self.labels_nonironic = FileOperations.convert_to_utf(FileOperations.read_file_json("../data/labels_nonironic.json"))
        self.feature_vectors_ironic = FileOperations.convert_to_utf(FileOperations.read_file_json("../data/feature_vectors_ironic.json"))
        self.labels_ironic = FileOperations.convert_to_utf(FileOperations.read_file_json("../data/labels_ironic.json"))


    def prepare_test_train_data(self):
        self.feature_vectors_nonironic = self.convert_dict_to_list(self.feature_vectors_nonironic)
        self.feature_vectors_ironic = self.convert_dict_to_list(self.feature_vectors_ironic)
        (self.X_train, self.X_test) = self.split_data(self.feature_vectors_ironic, self.feature_vectors_nonironic, TRAIN_TEST_SPLIT)
        (self.Y_train, self.Y_test) = self.split_data(self.labels_ironic, self.labels_nonironic, TRAIN_TEST_SPLIT)

    def split_data(self, ironic_data, nonironic_data, alpha):

        tt_split_index1 = int(alpha*len(nonironic_data))
        tt_split_index2 = int(alpha*len(ironic_data))

        train_data = nonironic_data[0:tt_split_index1]
        train_data.extend(ironic_data[0:tt_split_index2])

        test_data = nonironic_data[tt_split_index1:]
        test_data.extend(ironic_data[tt_split_index2:])

        return (np.array(train_data), np.array(test_data))

    def convert_dict_to_list(self, feature_vectors):
        dense_vectors = []
        count = 0
        for i in range(0,len(feature_vectors)):
            feature_vector_dense = []
            for feature in self.features:
                feature_vector_dense.append(feature_vectors[i][feature])
            dense_vectors.append(feature_vector_dense)
        return dense_vectors

    def train_classifier(self):
        self.classifier = LinearSVC(dual=True, class_weight="auto")
        self.classifier.fit(self.X_train,self.Y_train)


    def test_classifier(self):
        Y_obs = self.classifier.predict(self.X_test)
        print classification_report(self.Y_test, Y_obs)

def main(features):
    ir_classifier = IronyClassifier(features)
    ir_classifier.load_data()
    ir_classifier.prepare_test_train_data()
    ir_classifier.train_classifier()
    ir_classifier.test_classifier()

if __name__ == "__main__":
    if len(sys.argv)>1:
        FEATURES = []
        for arg in sys.argv[1:]:
            if arg.upper() in FEATURE_MAP:
                FEATURES.extend(FEATURE_MAP[arg.upper()])
            else:
                print "invalid argument"
                quit()

    main(FEATURES)
