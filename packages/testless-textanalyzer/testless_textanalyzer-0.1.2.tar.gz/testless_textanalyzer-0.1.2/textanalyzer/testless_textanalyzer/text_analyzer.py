import nltk
import re
import pickle
from textanalyzer.testless_textanalyzer.feature_set import * 

class TextAnalyzer():
    def __init__(self, path_to_model):
        self.model = pickle.load(open(path_to_model, 'rb'))
        self.feature_set = FeatureSet()
    

    def analyze(self, sentences):

        sentences_fetures = []

        processed_senteces = []

        for sentence in sentences:

            processed_text = self.text_processing(sentence)

            self.tokens, self.pos = self.text_tokenization_and_pos(
                processed_text)

            sentence_data = self.get_sentence_data()

            features =  self.feature_set.sent2features(sentence_data)

            sentences_fetures.append(features)

            processed_senteces.append(processed_text)

        predicted_entities = self.model.predict(sentences_fetures)

        return self.mapping_entities_to_words(processed_senteces, predicted_entities)

    def text_tokenization_and_pos(self, text):

        tokens = text.split()

        pos_tuple = nltk.pos_tag(tokens)

        pos_result = [pos[1] for index, pos in enumerate(pos_tuple)]

        return tokens, pos_result

    def text_processing(self, text):

        text = re.sub('[%s]' % re.escape(
            """!"#$%&'*,،;<>؟?[]^`{|}~"""), ' ', text)  # remove punctuation
        return text

    def get_sentence_data(self):

        sentence_data = []

        for token, word_pos in zip(self.tokens, self.pos):
            sentence_data.append((token, word_pos))
            
        return sentence_data

    def sent2features(self, sent):
        
        return [self.word2features(sent, i) for i in range(len(sent))]

    def word2features(self, sent, i):
        
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

    def mapping_entities_to_words(self, sentences, predicted_entities):
        result = []
        for sentence, entities in zip(sentences, predicted_entities):
            senntence_words = sentence.split()
            sentence_entities = {}
            ass, act, targ, val = '', '', '', ''
            'targ', 'val'
            for word, entity in zip(senntence_words, entities):
                if entity.endswith('assert'):
                    ass += word + ' '
                elif entity.endswith('act'):
                    act += word + ' '
                elif entity.endswith('targ'):
                    targ += word + ' '
                elif entity.endswith('val'):
                    val += word + ' '

            if val != '':
                sentence_entities["value"] = val.strip()
            if targ != '':
                sentence_entities["target"] = targ.strip()
            if act != '':
                sentence_entities["action"] = act.strip()
            if ass != '':
                sentence_entities["assertion"] = ass.strip()

            result.append(sentence_entities)

        return result
