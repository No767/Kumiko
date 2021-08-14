FROM python:3.10.0b4-slim-buster
WORKDIR /Bot
COPY . .
RUN pip install -r requirements.txt
ENTRYPOINT ["python rinbot.py"]
