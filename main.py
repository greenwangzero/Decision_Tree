import pandas as pd
import numpy as np
from sklearn import preprocessing
from sklearn.metrics import log_loss
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import BernoulliNB
train = pd.read_csv('C:/Users/green/Desktop/train.csv', parse_dates = ['Dates'])
test = pd.read_csv('C:/Users/green/Desktop/test.csv', parse_dates = ['Dates'])
features=['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday', 'BAYVIEW', 'CENTRAL', 'INGLESIDE', 'MISSION',
 'NORTHERN', 'PARK', 'RICHMOND', 'SOUTHERN', 'TARAVAL', 'TENDERLOIN']


def Preprocess():
    # Category
    category = preprocessing.LabelEncoder()
    primeCategory = category.fit_transform(train.Category)
    #
    days = pd.get_dummies(train.DayOfWeek)
    district = pd.get_dummies(train.PdDistrict)
    hour = train.Dates.dt.hour
    hour = pd.get_dummies(hour)
    trainData = pd.concat([hour, days, district], axis=1)  # 将特征进行横向组合
    #print(trainData)
    trainData['crime'] = primeCategory  # 追加'crime'列
    days = pd.get_dummies(test.DayOfWeek)
    district = pd.get_dummies(test.PdDistrict)
    hour = test.Dates.dt.hour
    hour = pd.get_dummies(hour)
    testData = pd.concat([hour, days, district], axis=1)
    # print(trainData)
    return trainData, testData

def Train(trainData):
    X_train, X_test, y_train, y_test = train_test_split(trainData[features], trainData['crime'])
    NB = BernoulliNB()
    NB.fit(X_train, y_train)

    propa = NB.predict(X_test)
    predicted = np.array(propa)
    logLoss = log_loss(y_test, predicted)
    print("朴素贝叶斯的log损失为:%.6f" % logLoss)

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    trainData,testData = Preprocess()
    Train(trainData)

# See PyCharm help at https://www.jetbrains.com/help/pycharm/