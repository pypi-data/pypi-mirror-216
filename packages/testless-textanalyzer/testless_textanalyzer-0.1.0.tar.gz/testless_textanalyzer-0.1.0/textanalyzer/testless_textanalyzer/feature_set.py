class FeatureSet():
    # A class to retrieve the features from the dataset and prepare them for training
    def __init__(self, data = None):
        self.data = data
        self.X = None
        self.y = None
        

    def get_X(self):
        self.calculate_features()

        # return the features
        return self.X
    
    def get_y(self):
        self.calculate_labels()

        # return the labels
        return self.y
    
    def get_data(self):
        # return the data
        return self.data
    
    def calculate_features(self):
        if self.X is not None:
            return
        
        # calculate the features
        self.X = [self.sent2features(s) for s in self.data]

    def calculate_labels(self):
        if self.y is not None:
            return
        
        # calculate the labels
        self.y = [self.sent2labels(s) for s in self.data]
    
    def sent2features(self, sent):
        # return the features for a single sentence
        return [self.word2features(sent, i) for i in range(len(sent))]
    
    def sent2labels(self,sent):
        # return the labels for a single sentence
        return [label for token, postag, label in sent]
    
    def word2features(self, sent, i):
        # return the features for a single word
        word = sent[i][0]
        postag = sent[i][1]

        features = {
            'bias': 1.0,
            'word.lower()': word.lower(),
            'word[-3:]': word[-3:],
            'word[-2:]': word[-2:],
            'postag': postag,
            'postag[:2]': postag[:2],
        }
        if i > 0:
            word1 = sent[i-1][0]
            postag1 = sent[i-1][1]
            features.update({
                '-1:word.lower()': word1.lower(),
                '-1:postag': postag1,
                '-1:postag[:2]': postag1[:2],
            })
        else:
            features['BOS'] = True

        if i < len(sent)-1:
            word1 = sent[i+1][0]
            postag1 = sent[i+1][1]
            features.update({
                '+1:word.lower()': word1.lower(),
                '+1:postag': postag1,
                '+1:postag[:2]': postag1[:2],
            })
        else:
            features['EOS'] = True

        return features

