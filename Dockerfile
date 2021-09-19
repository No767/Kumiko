FROM python:3.9.7
WORKDIR /Bot
COPY requirements.txt ./ /Bot/
RUN pip install --upgrade pip setuptools wheel
RUN pip install -r requirements.txt 
CMD ["python", "./Bot/rinbot.py"]
