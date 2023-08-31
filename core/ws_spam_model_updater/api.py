import os
from datetime import datetime, timedelta

import joblib
from flask import Blueprint, jsonify, request
from sklearn.feature_extraction.text import TfidfVectorizer

from core.email_spam_analyzer import EmailSpamAnalyzer
from core.utils.db_manager import DbManager

urls_blueprint = Blueprint('api_urls', __name__)

@urls_blueprint.route('/', methods=['GET'])
def home2():
    return 'Page par defaut', 200

@urls_blueprint.route('/spam-email-refine/api/v1.0', methods=['GET'])
def home():
    return 'Welcome to this web service\nThe aim is for you to refine an email that was classified as ham or spam.', 200

@urls_blueprint.route('/spam-email-refine/api/v1.0/define-email-classification', methods=['POST'])
def refine_model_email():
    payload = request.get_json(force=True)
    if 'email' not in payload.keys():
        result = {'status':'ko','message':'no email found in the payload.'}
        return jsonify(result), 200
    
    if 'classification' not in payload.keys():
        result = {'status':'ko','message':'no email classification found in the payload.'}
        return jsonify(result), 200
    
    if 'ham' in payload['classification'].lower() or payload['classification'][0:1] == "0" :
        payload['classification'] = "0"
    else:
        payload['classification'] = "1"

    email_to_analyze = payload['email']
    email_classification = payload['classification']
    message_status = 'spam' if email_classification == "1" else 'ham'
    user_ip_address = request.remote_addr
    
    dbManager = DbManager()
    dbManager.connect()
    if not dbManager.exist_email(email_to_analyze):
        dbManager.add_email(email=email_to_analyze,tag=message_status,ip_address=user_ip_address,comment='valid add email operation')

        spam_data_file = open("core/machine_learning/data/spam.csv", "a") 
        spam_data_file.write('\n"' + email_classification + '","' + email_to_analyze + '"')
        spam_data_file.close()        
        
        result = {'status':'ok','message':'your email has been added as {}'.format(message_status)}
    else:
        dbManager.add_rejected_email(email=email_to_analyze,tag=message_status,ip_address=user_ip_address,comment='invalid already exsiting email.')
        result = {'status':'ok','message':'your email will be taken into account.'}

    return jsonify(result), 200

@urls_blueprint.route('/spam-email-refine/api/v1.0/generate_model', methods=['GET'])
def regenerate_model():

    datenow = datetime.now()
    last_model_creation_time = datetime.fromtimestamp(os.path.getctime('core/machine_learning/ml_model_export/email_spam_detector_model.joblib'))
    one_day = timedelta(days=1)

    if datenow - last_model_creation_time > one_day:
        email_spam_analyzer = EmailSpamAnalyzer('core/machine_learning/data/spam.csv')
        email_spam_analyzer.sanitize_data()
        email_spam_analyzer.generate_model()
        email_spam_analyzer.train_model()
        email_spam_analyzer.save_model()
    
    return jsonify({'status':'ok'}), 200

@urls_blueprint.route('/spam-email-refine/api/v1.0/my_email_is_spam_or_ham', methods=['POST'])
def check_email():
    payload = request.get_json(force=True)
    if 'email' not in payload.keys():
        result = {'status':'ko','message':'no email found in the payload.'}
        return jsonify(result), 200

    email_to_analyze = payload['email']
    email = [email_to_analyze]

    SVM = joblib.load('core/machine_learning/ml_model_export/email_spam_detector_model.joblib')
    tf_vec = joblib.load('core/machine_learning/ml_model_export/tf_vectorizer.joblib')
    email_transfromed = tf_vec.transform(email)
    
    result = SVM.predict(email_transfromed)

    if str(result.item()) == "0":
        return jsonify({'status':'ok','classification':'ham','email':email_to_analyze}), 200
    elif str(result.item()) == "1":
        return jsonify({'status':'ok','classification':'spam','email':email_to_analyze}), 200
    else:
        return jsonify({'status':'ko','classification':'this email can not be auto-classified yet.\nHint: you could set its classification for refining purposes by calling "define-email-classification"','email':email_to_analyze}), 200

    
