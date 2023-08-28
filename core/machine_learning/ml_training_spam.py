import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
import joblib
from sklearn.metrics import accuracy_score

class MLSpamTrainer():

    def __init__(self, dataset_path:str, dataset_test_rate=0.3) -> None:
        self.dataset_path = dataset_path
        self.dataset_test_rate = self._validate_rate(dataset_test_rate)
        self.data = None
        self.model = None
        self.analytics = None

    def _validate_rate(self, value:int) -> float:
        if value > 1:
            return value / 100
        return value

    def init_data(self) -> bool:
        try:
            df = pd.read_csv(self.dataset_path, quotechar="\"",engine='python')
            self.data = df.where(pd.notnull(df),'')
            return True
        except FileNotFoundError as e:
            print(str(e))
            return False
        
    def _set_location(self) -> dict:
        self.data.loc[self.data['Label'] == 'spam', 'Label',] = 0  # email is spam, value is 0
        self.data.loc[self.data['Label'] == 'ham', 'Label',] = 1   # emails is valid, value is 1

        X = self.data['EmailText']
        Y = self.data['Label']
        x_training, x_test, y_training, y_test = train_test_split(X,Y,test_size=self.dataset_test_rate,random_state=0)

        y_training = y_training.astype('int')
        y_test = y_test.astype('int')

        return {'x_training':x_training, 'x_test':x_test, 'y_training':y_training, 'y_test':y_test}
    
    def _extract_features(self, locations:dict) -> dict:
        feature_extraction = TfidfVectorizer(min_df=1,stop_words='english',lowercase=True)

        x_training_features = feature_extraction.fit_transform(locations['x_training'])
        x_test_features = feature_extraction.transform(locations['x_test'])

        return {'feature_extraction':feature_extraction, 'x_training_features':x_training_features, 'x_test_features':x_test_features}
    
    def get_analytics(self) -> dict:
        locations = self._set_location()
        features = self._extract_features(locations)
        self.analytics = locations | features
        return self.analytics

    def create_model(self) -> bool:
        self.model = LogisticRegression()
        self.model.fit(self.analytics['x_training_features'], self.analytics['y_training'])
        return True

    def save_model(self,filename:str='ML_spam_model.bin') -> bool:
        if filename:
            joblib.dump(self, 'core/machine_learning/ml_model_export/' + filename)
            return True
        else:
            return False
    
    def model_accuracy_on_training_data(self):
        prediction_on_training_data = self.model.predict(self.analytics['x_training_features'])
        return accuracy_score(self.analytics['y_training'], prediction_on_training_data)

    def model_accuracy_on_test_data(self):
        prediction_on_test_data = self.model.predict(self.analytics['x_test_features'])
        return accuracy_score(self.analytics['y_test'], prediction_on_test_data)

    def is_spam_email(self,email:list):
        input_data_features = self.analytics['feature_extraction'].transform(email)
        if self.model.predict(input_data_features) == 1:
            return False
        
        return True



    