FROM python:3.10-rc-slim
WORKDIR /Bot
COPY . .
RUN pip install -r requirements.txt
ENTRYPOINT ["python rinbot.py"]
