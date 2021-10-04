FROM python:3.9.7
WORKDIR /Bot
COPY Pipfile ./ /Bot/
COPY Pipfile.lock ./ /Bot/
RUN pip install --upgrade pip setuptools wheel
RUN pip install pipenv
RUN pipenv install
CMD ["pipenv", "run", "python", "./Bot/rinbot.py"]