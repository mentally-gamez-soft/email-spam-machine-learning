from flask import Flask, request, jsonify
import joblib

web_service_api = Flask(__name__)

@web_service_api.route('/', methods=['GET'])
def home():
    return 'Home page', 200

@web_service_api.route('/spam-email-control/api/v1.0', methods=['GET','POST'])
def analyze_email():
    payload = request.get_json(force=True)

    email_to_analyze = payload['email']
    email_to_analyze = [email_to_analyze]
    print('EMAIL => ' + email_to_analyze[0])

    model = joblib.load('core/machine_learning/ml_model_export/ML_spam_model.bin')
    print('model loaded correctly')

    result = {'status':'ko','email':email_to_analyze}
    
    if model.is_spam_email(email=email_to_analyze):
        result = {'status':'ok','email_status':'spam','email':email_to_analyze}
    else:
        result = {'status':'ok','email_status':'ham','email':email_to_analyze}

    return jsonify(result), 200

