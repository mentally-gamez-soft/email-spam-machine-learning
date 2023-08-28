FROM python:3.10-bookworm

LABEL Name="WS to update spam email model (flask app)" Version=0.0.1

WORKDIR /ws-spam-model
COPY requirements.in .
RUN python -m pip install --upgrade pip
RUN pip install pip-tools
RUN pip-compile requirements.in
RUN pip install --no-cache-dir -r requirements.txt

COPY app.py .
COPY core/machine_learning/data/spam_essai.csv ./core/machine_learning/data/spam_essai.csv
COPY core/ws_spam_model_updater ./core/ws_spam_model_updater

EXPOSE 5000

CMD ["gunicorn", "-b", "0.0.0.0:5000", "app:app"]
# CMD ["python", "app.py"]
