FROM python:3.10.8-slim-bullseye

RUN python3 -m venv /opt/venv

# Install dependencies:
COPY requirements.txt .
RUN /opt/venv/bin/pip install -r requirements.txt

# Run the application:
COPY . .
CMD /opt/venv/bin/python main.py
