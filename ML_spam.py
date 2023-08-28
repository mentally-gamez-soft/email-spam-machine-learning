import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer
from sklearn import svm  # Support Vector Machine algorithm
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import make_pipeline
from sklearn.metrics import accuracy_score

spam = pd.read_csv('core/machine_learning/data/spam.csv')


print('step 0')
print(spam) 


z = spam['EmailText'].values.astype(str) #assigns the column EmailText from spam to z. It contains the data that we’ll run through the model. 
y = spam["Label"].values  # assigns the column Label from spam to y, telling the model to correct the answer. 

print('step 1')

#The function z_train, z_test,y_train, y_test = train_test_split(z,y,test_size = 0.2) 
# divides columns z and y into z_train for training inputs, y_train for training labels, z_test for testing inputs, 
# and y_test for testing labels.
# test_size=0.2 sets the testing set to 20 percent of z and y
z_train, z_test, y_train, y_test = train_test_split(z,y,test_size = 0.2, random_state=0) 
print(z_train.shape)
print(z_test.shape)
print('step 2')
print(y_train.shape)
print(y_test.shape)
 
# CountVectorizer() randomly assigns a number to each word in a process called tokenizing. 
# Then, it counts the number of occurrences of words and saves it to cv. 
# At this point, we’ve only assigned a method to cv
# PREPROCESSING
cv = CountVectorizer()

print('step 3')

# Training ML Algorithm
nb = MultinomialNB()

pipe = make_pipeline(cv, nb)
print('step 4')

pipe.fit(z_train, y_train)
print('step 5')

y_pred = pipe.predict(z_test)
print('step 6')

accuracy = accuracy_score(y_pred, y_test)
print(accuracy)

email = ['URGENT! You have won a 1 week FREE membership in our £100']
print(pipe.predict(email))


# # randomly assigns a number to each word. It counts the number of occurrences of each word, then saves it to cv.
# features = cv.fit_transform(z_train)

# print('step 4')

# model = svm.SVC() # assigns svm.SVC() to the model

# print('step 5')

# # model.fit trains the model with features and y_train. 
# # Then, it checks the prediction against the y_train label and adjusts its parameters until it reaches the highest possible accuracy
# model.fit(features,y_train)    

# print('step 6')

# features_test = cv.transform(z_test)
# print("Accuracy: {}".format(model.score(features_test,y_test)))




# # # Fitting Simple Linear Regression to the Training set
# # from sklearn.linear_model import LinearRegression
# # regressor = LinearRegression()
# # regressor.fit(z_train, y_train)
# print('step 7')
# # # Predicting the Test set results
# l_data = ['Hello world',]
# # y_pred = regressor.predict(l_data)

# model.predict(l_data)