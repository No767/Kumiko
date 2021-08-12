FROM python:3.9.6
WORKDIR /Bot
COPY . .
RUN pip install -r requirements.txt
ENTRYPOINT ["python rinbot.py"]
