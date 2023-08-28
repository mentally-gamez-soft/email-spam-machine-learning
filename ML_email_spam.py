import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score

df = pd.read_csv('core/machine-learning/data/spam.csv')
print(df)


data = df.where(pd.notnull(df),'')
# print(data.head(20))
# print(data.info)

data.loc[data['Label'] == 'spam', 'Label',] = 0
data.loc[data['Label'] == 'ham', 'Label',] = 1

X = data['EmailText']
Y = data['Label']

X_train, X_test, Y_train, Y_test = train_test_split(X,Y,test_size=0.2,random_state=3) 

# print(X.shape)
# print(X_train.shape)
# print(X_test.shape)

# print(Y.shape)
# print(Y_train.shape)
# print(Y_test.shape)
 
feature_extraction = TfidfVectorizer(min_df=1,stop_words='english',lowercase=True)

X_train_features = feature_extraction.fit_transform(X_train)

X_test_features = feature_extraction.transform(X_test)

Y_train = Y_train.astype('int')
Y_test = Y_test.astype('int')
# print(X_train)
# print(X_train_features)

model = LogisticRegression()
model.fit(X_train_features, Y_train)


prediction_on_training_data = model.predict(X_train_features)
accuracy_on_training_data = accuracy_score(Y_train, prediction_on_training_data)
print(accuracy_on_training_data)

prediction_on_test_data = model.predict(X_test_features)
accuracy_on_test_data = accuracy_score(Y_test, prediction_on_test_data)
print(accuracy_on_test_data)


# creation of the predictive system
input_your_mail = ["Hey there, I just found your site, quick question…"]

input_data_features = feature_extraction.transform(input_your_mail)

prediction = model.predict(input_data_features)

print(prediction)