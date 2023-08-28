import nltk
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns 
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from sklearn.svm import SVC 
from core.utils.data_sanitizer import DataSanitizer
from nltk.corpus import stopwords
from wordcloud import WordCloud
import pickle

# import warnings
# warnings.filterwarnings('ignore')

def setup_nltk():
    nltk.download('stopwords')
    nltk.download('wordnet')
    nltk.download('punkt')
    nltk.download('averaged_perceptron_tagger')

#setup_nltk()


# load the dataset
df = pd.read_csv('core/machine_learning/data/spam_test.csv')
print(df.head())
print(df.info())
print('shape of dataset', df.shape)
print(df.isnull().sum())
print('count of label:\n',df['Label'].value_counts())

# Checking the ratio of labels
print('not a spam email ratio is: ', round(len(df[df['Label']=='ham'])/len(df['Label']),2)*100,'%')
print('Spam email ratio is: ', round(len(df[df['Label']=='spam'])/len(df['Label']),2)*100,'%')

df['length'] = df.EmailText.str.len()
#print(df.head())

df['EmailText'] = df['EmailText'].str.lower()
#print(df.head())

# Replacing each email by the phrase emailaddress
# data_sanitizer = DataSanitizer(df['EmailText'].str)
#print('INIT DONE.')

df['EmailText'] = df['EmailText'].str.replace(r"[a-zA-Z0-9.!#$%&'*+/=?^_`{|}~-]+@[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?(?:\.[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?)*", 'emailaddress', regex=True)
#df['message'] = data_sanitizer.sanitize_email()
print('>>>>>  EMAIL <<<<<<<<<<<<')
print(df.head())
print('*******************************************************************************')

# Replacing urls by the phrase webaddress
df['EmailText'] = df['EmailText'].str.replace(r'http(s){0,1}\://[a-zA-Z0-9\-\.]+\.[a-zA-Z]{2,3}(/\S*)\b', 'webaddress', regex=True)
# df['message'] = data_sanitizer.sanitize_web_url(overwright_text=True)
print('>>>>>  URL <<<<<<<<<<<<')
print(df.head())
print('*******************************************************************************')

# Replacing currency symbols by the phrase moneysymb
df['EmailText'] = df['EmailText'].str.replace(r'£|\$|€', 'dollars', regex=True)
print('>>>>>  CURRENCY <<<<<<<<<<<<')
print(df.head())
print('*******************************************************************************')

# Replacing 10 digits phone nmber with the phrase phonenumber
df['EmailText'] = df['EmailText'].str.replace(r'(^(\+\d{1,2}\s)?\(?\d{3}\)?[\s.-]\d{3}[\s.-]\d{4}$)|^\(?[\d]{3}\)?[\s-]?[\d]{3}[\s-]?[\d]{4}$', 'phonenumber', regex=True)
print('>>>>>  PHONE <<<<<<<<<<<<')
print(df.head())
print('*******************************************************************************')

# Replacing numeric chars by the phrase number
df['EmailText'] = df['EmailText'].str.replace(r'\d+(\.\d+)?','number', regex=True)
print('>>>>>  NUMBER <<<<<<<<<<<<')
print(df.head())
print('*******************************************************************************')

# remove punctuations
df['EmailText'] = df['EmailText'].str.replace(r'[^\w\d\s]','', regex=True)
print('>>>>>  PUNCTUATION <<<<<<<<<<<<')
print(df.head())
print('*******************************************************************************')

# replace whitespace by one single space
df['EmailText'] = df['EmailText'].str.replace(r'\s+',' ', regex=True)
print('>>>>>  WHITESPACES <<<<<<<<<<<<')
print(df.head())
print('*******************************************************************************')

# remove leading and trailing whitespace
df['EmailText'] = df['EmailText'].str.replace(r'^\s+?$','', regex=True)
print('>>>>>  WHITESPACES 2 <<<<<<<<<<<<')
print(df.head())
print('*******************************************************************************')


# remove stopwords
stopwords = set(stopwords.words('english')+['u','ur','4','2','im','dont','doin','ure','ü'])
df['EmailText'] = df['EmailText'].apply(lambda x:" ".join(term for term in x.split() if term not in stopwords))

# new column (clean_length) after stopwords removal
df['clean_length'] = df.EmailText.str.len()
print(df.head())

# total length removal
print("original length:", df.length.sum())
print("cleaned length:", df.clean_length.sum())
print("total words removed:", (df.length.sum()- df.clean_length.sum()))

# graphical vizualisation for counting number of Label
plt.figure(figsize=(6,4))
sns.countplot(df['Label'], palette='Reds')
plt.title('Counting the number of labels', fontsize=15)
plt.xticks(rotation='horizontal')
plt.show()
print(df.Label.value_counts())


# message distribution
f, ax = plt.subplots(1,2,figsize=(15,8))
sns.distplot(df[df['Label']==1]['length'],bins=20,ax=ax[0],label='Spam Message Distribution',color='r')
ax[0].set_xlabel('spam message length')
ax[0].legend()

sns.distplot(df[df['Label']==0]['length'],bins=20,ax=ax[1],label='No Spam Message Distribution',color='b')
ax[1].set_xlabel('No spam message length')
ax[1].legend()

plt.show()


f,ax  = plt.subplots(1,2,figsize=(15,8))
sns.distplot(df[df['Label']==1]['clean_length'],bins=20,ax=ax[0],label='Spam Message Distribution',color='y')
ax[0].set_xlabel('spam message length')
ax[0].legend()

sns.distplot(df[df['Label']==0]['clean_length'],bins=20,ax=ax[1],label='No Spam Message Distribution',color='g')
ax[1].set_xlabel('No spam message length')
ax[1].legend()

plt.show()

# visualization of spam data via wordcloud
spams = df['EmailText'][df['Label']==1]

spam_cloud = WordCloud(width=800,height=500,background_color='white',max_words=200).generate(''.join(spams))
plt.figure(figsize=(10,8),facecolor='b')
plt.imshow(spam_cloud)
plt.axis('off')
plt.tight_layout(pad=0)
plt.show()


# visualization of non spam data via wordcloud
no_spams = df['EmailText'][df['Label']==0]

no_spam_cloud = WordCloud(width=800,height=500,background_color='white',max_words=200).generate(''.join(no_spams))
plt.figure(figsize=(10,8),facecolor='b')
plt.imshow(spam_cloud)
plt.axis('off')
plt.tight_layout(pad=0)
plt.show()

# 1. Convert all texts into vectors using TF-IDF
# 2. Instantiate MultinomialNB classifier
# 3. Split feature and label
tf_vec = TfidfVectorizer()
SVM = SVC(C=1.0,kernel='linear',degree=3,gamma='auto')
features = tf_vec.fit_transform(df['EmailText'])

x = features
y = df['Label']

x_train, x_test, y_train, y_test = train_test_split(x,y,random_state=42)
SVM.fit(x_train,y_train)
y_pred = SVM.predict(x_test)
print('final score: ', accuracy_score(y_test, y_pred))

print(classification_report(y_test, y_pred))

# visualization of the confusion matrix heatmap
conf_mat = confusion_matrix(y_test,y_pred)
ax = plt.subplot()
sns.heatmap(conf_mat,annot=True,ax=ax,linewidths=5,linecolor='g',center=0)
ax.set_xlabel('predicted labels')
ax.set_ylabel('True labels')
ax.set_title('Confusion Matrix')
ax.xaxis.set_ticklabels(['not spam','spam'])
ax.yaxis.set_ticklabels(['not spam','spam'])
plt.show()


# saving the model 
file_name = 'core/machine_learning/ml_model_export/Email_spam_detect.pkl'
M = open(file_name, 'wb')
pickle.dump(SVM,M)
M.close()


# test model
email = ["Dear Infura user,\
\
We recently heard from a few users who reported having received phishing emails that impersonated Infura, with claims of offering high staking rewards for converting ETH to ETH 2.0. \
\
\
\
Infura is not associated with these malicious actors and does NOT offer any staking products at this time.\
\
\
\
Protect yourself from these scams:\
\
Always confirm the legitimacy of an email by checking on the email address of the sender. The email domain should match our official website domains, infura.io or consensys.net\
If in doubt, reach out to us at support@infura.io to confirm new features or promotions\
Be wary of any unexpected emails and offers that ask you to act quickly to get a reward\
Refrain from connecting your crypto wallets to non-credible sites or sources\
Never give anyone your seed phrase or passwords\
Never click on suspicious links\
Install a reputable antivirus and browsing protection on your device\
Sincerely,\
\
The Infura Team"]
print(SVM.predict(tf_vec.transform(email)))
