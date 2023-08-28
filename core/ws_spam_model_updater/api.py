from flask import Flask, request, jsonify
from __init__ import create_app

# web_service_api = Flask(__name__)
web_service_api = create_app()

@web_service_api.route('/spam-email-refine/api/v1.0', methods=['GET'])
def home():
    return 'Welcome to this web service\nThe aim is for you to refine an email that was classified as ham or spam.', 200

@web_service_api.route('/spam-email-refine/api/v1.0/redifine-email', methods=['POST'])
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
    
    spam_data_file = open("core/machine_learning/data/spam_essai.csv", "a") 
    spam_data_file.write('\n"' + email_classification + '","' + email_to_analyze + '"')
    spam_data_file.close()
    message_status = 'spam' if email_classification == "1" else 'ham'
    result = {'status':'ok','message':'your email has been added as {}'.format(message_status)}

    return jsonify(result), 200
