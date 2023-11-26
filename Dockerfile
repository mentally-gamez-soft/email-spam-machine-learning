FROM python:3.11.6-bookworm

# Install vi editor in container
RUN apt-get update && apt-get install -y vim net-tools

LABEL Name="Email Scoring Flask APP" Version=$version_number

WORKDIR /ws-email-scoring
COPY requirements.in .
COPY requirements-dev.in .
RUN python -m pip install --upgrade pip
RUN pip install pip-tools
RUN pip-compile --output-file=requirements.txt requirements.in
RUN pip-compile --output-file=requirements-dev.txt requirements-dev.in
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install --no-cache-dir -r requirements-dev.txt

# root application directory
COPY .env .
COPY .env.vault .
COPY app.py .

# application core
COPY core ./core

# application tests
COPY tests ./tests

# statis
COPY static ./static

EXPOSE 5000

CMD ["gunicorn", "-b", "0.0.0.0:5000", "app:app"]
