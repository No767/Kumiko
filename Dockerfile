FROM python:3.10.0
WORKDIR /Bot
COPY Pipfile ./ /Bot/
COPY Pipfile.lock ./ /Bot/
RUN chmod -R 777 /Bot
RUN pip install --upgrade pip pipenv
RUN pipenv install
CMD ["pipenv", "run", "python", "./Bot/rinbot.py"]