FROM python:3.9.6

WORKDIR /

RUN pip install discord 

RUN pip install python-dotenv

RUN python main.py

CMD ["python", "main.py", "pip"]