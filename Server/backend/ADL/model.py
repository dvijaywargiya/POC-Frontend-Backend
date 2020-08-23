import time
import pandas
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.utils import check_array
from sklearn.neural_network import MLPRegressor
from sklearn.preprocessing import MinMaxScaler
import statistics
from backend.db.connection import container_jobs
import numpy as np

categoryMap = {
    'MSIT': 0,
    'Commercial': 1,
    'Personal': 2,
    'Consumer': 3
}

datasetMap = {
    "Calendar": 0,
    "Documents": 1,
    "Forms": 2,
    "MailFolders": 3,
    "Emails": 4,
    "TeamsConversation": 5,
    "SIGSAcronyms": 6,
    "SIGSCortana": 7,
    "SIGSMeetingTranscriptInsights": 8,
    "SIGSOXO": 9,
    "SIGSSmartCompose": 10,
    "SIGSSmartReply": 11,
    "SIGSSpeechServices": 12,
    "SIGSSuggestedTask": 13,
    "CuratedActions": 14,
    "CuratedCalendar": 15,
    "CuratedDocuments": 16,
    "CuratedMailFolders": 17,
    "CuratedEmails": 18,
    "CuratedPeople": 19,
    "ReplyPrediction": 20,
    "CIVPrime": 21,
    "SIGSOIVIC": 22,
    "CuratedEmailReplyPair": 23,
    "CuratedTeamsConversation": 24,
    "CuratedUser": 25,
    "FocusedInbox": 26,
}

class Model:
    def __init__(self):
        self.regressor = MLPRegressor(hidden_layer_sizes = (5, 10, 5), activation = 'relu', solver = 'sgd', learning_rate = 'adaptive')
        self.mean = 0
        self.sd = 0
        self.scalarX = MinMaxScaler()
        self.scalarY = MinMaxScaler()
        self.reTrain()

    def reTrain(self):
        item_list = list(container_jobs.read_all_items())
        X = []
        Y = []
        for ele in item_list:
            lt1 = []
            lt1.append(categoryMap[ele['category']])
            try:
                lt1.append(datasetMap[ele['entityName']])
            except:
                lt1.append(27)    
            lt1.append(ele['day'])
            lt1.append(ele['time'])
            lt1.append(ele['days'])
            Y.append(ele['timeTaken'])
            X.append(lt1)
        X = np.array(X)
        Y = np.array(Y)

        self.mean = sum(Y)/len(Y)
        self.sd = statistics.stdev(Y)
        lenY = len(Y)
        X = self.scalarX.fit_transform(X)
        Y = self.scalarY.fit_transform(Y.reshape(lenY, 1))
        Y = Y.reshape(lenY, )
        regressor = MLPRegressor(hidden_layer_sizes = (5, 10, 5), activation = 'relu', solver = 'sgd', learning_rate = 'adaptive')
        regressor.fit(X, Y)
        self.regressor = regressor


    def predict(self, input):
        Xnew = self.scalarX.transform(input)
        prediction = self.regressor.predict(Xnew)
        ret = []
        for ele in prediction:
            ret.append(round((ele*self.sd + self.mean)/2, 2))
        return ret

Regressor = Model()