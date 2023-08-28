from core.machine_learning.ml_training_spam import MLSpamTrainer

def test_model(model):
    email = ['renew your vitality  for the first time']
    if model.is_spam_email(email=email):
        print('the test email is a spam as expected.')
    else:
        print('the test email is valid but its supposed to be detected as a spam.')

app_model_training = MLSpamTrainer('core/machine_learning/data/spam.csv',0.4)
if app_model_training.init_data():
    app_model_training.get_analytics()
    app_model_training.create_model()
    accuracy_training_data = app_model_training.model_accuracy_on_training_data()
    accuracy_test_data = app_model_training.model_accuracy_on_test_data()

    if accuracy_training_data >= 0.9 and accuracy_test_data >= 0.9:
        app_model_training.save_model('latest_model_version_20230824.bin')

        test_model(app_model_training)
    else:
        print('accuracy for training is {}, accuracy for testing is {}, is lower than 0.95, the model cant be saved'.format(accuracy_training_data,accuracy_test_data))



