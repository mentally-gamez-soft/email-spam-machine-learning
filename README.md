# Machine learning API for email spam classifier [![Spam Emails Machine Learning Trainer](https://github.com/mentally-gamez-soft/email-spam-machine-learning/actions/workflows/spam_ml_training.yaml/badge.svg?branch=main)](https://github.com/mentally-gamez-soft/email-spam-machine-learning/actions/workflows/spam_ml_training.yaml) 


## This project covers the following topics
 - How to correctly package a python project 
 - How to use natural language in python to classify emails as Spam or Ham
 - How to use docker and build an image of this project
 - How to define a workflow pipeline with github actions from unit testing till deployment on a dev server
 - How to write an API in Flask 
 - How to use unittest
 - How to use swagger documentation with Flask


# Definitions des endoints
    http://167.86.83.102:5000/swagger

### Endpoint http://167.86.83.102:5000/spam-email-refine/api/v1.0/define-email-classification

    Define or refine the classification of an email. The end user must provide an email and a status ['ham','spam'] 

### Endpoint http://167.86.83.102:5000/spam-email-refine/api/v1.0/generate_model

    This will trigger a regeneration of the model to take into account any fresh data in the dataset.
    The refresh of the model can be triggered only once per day.

### Endpoint http://167.86.83.102:5000/spam-email-refine/api/v1.0/my_email_is_spam_or_ham

    The end user provides an email and the web service will respond according to its model learnt if it is known as a spam or a ham.
