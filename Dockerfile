FROM python:3.10-bookworm

LABEL Name="WS to update spam email model (flask app)" Version=0.1.0

WORKDIR /ws-spam-model
COPY requirements.in .
RUN python -m pip install --upgrade pip
RUN pip install pip-tools
RUN pip-compile requirements.in
RUN pip install --no-cache-dir -r requirements.txt

COPY app.py .
COPY core/__init__.py ./core/__init__.py
COPY core/email_spam_analyzer.py ./core/email_spam_analyzer.py
COPY static ./static
COPY core/utils ./core/utils
COPY core/machine_learning/data/spam.csv ./core/machine_learning/data/spam.csv
COPY core/ws_spam_model_updater ./core/ws_spam_model_updater
COPY core/machine_learning/ml_model_export/email_spam_detector_model.joblib ./core/machine_learning/ml_model_export/email_spam_detector_model.joblib

EXPOSE 5000

CMD ["gunicorn", "-b", "0.0.0.0:5000", "app:app"]
# CMD ["python", "app.py"]
