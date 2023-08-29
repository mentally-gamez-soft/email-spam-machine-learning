import os
from datetime import datetime, timedelta

from flask import Blueprint, jsonify, request

from core.email_spam_analyzer import EmailSpamAnalyzer

urls_blueprint = Blueprint('api_urls', __name__)

@urls_blueprint.route('/', methods=['GET'])
def home2():
    return 'Page par defaut', 200

@urls_blueprint.route('/spam-email-refine/api/v1.0', methods=['GET'])
def home():
    return 'Welcome to this web service\nThe aim is for you to refine an email that was classified as ham or spam.', 200

@urls_blueprint.route('/spam-email-refine/api/v1.0/define-email', methods=['POST'])
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
    # print('email_to_analyze 1 => ' + email_to_analyze)
    email_classification = payload['classification']
    # print('email_classification 1 => ' + email_classification)

    # email_to_analyze = [email_to_analyze]
    # print('email_to_analyze 2  => ' + email_to_analyze[0])
    # email_classification = [email_classification]
    # print('email_classification 2 => ' + email_classification[0])
    
    spam_data_file = open("core/machine_learning/data/spam.csv", "a") 
    spam_data_file.write('\n"' + email_classification + '","' + email_to_analyze + '"')
    spam_data_file.close()
    message_status = 'spam' if email_classification == "1" else 'ham'
    result = {'status':'ok','message':'your email has been added as {}'.format(message_status)}

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
