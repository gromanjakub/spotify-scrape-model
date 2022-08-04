import pandas as pd
from distutils.log import Log
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
from sklearn import preprocessing
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC

import scrape_final #import scrape_preload, get_ids, get_features

scrape_final.scrape_preload()
scrape_final.get_ids()
scrape_final.get_features()


X = df.drop(columns = ["id","liked"], axis = 1)
X_normalized = preprocessing.normalize(X)

y = df["liked"]
X_train, X_test, y_train, y_test = train_test_split(X_normalized,y, test_size=0.2, stratify = y)

models = [LogisticRegression(), RandomForestClassifier(), SVC(), GradientBoostingClassifier()]
for model in models:
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    print(str(model) + " accuracy score: " + str(accuracy_score(y_pred,y_test)))