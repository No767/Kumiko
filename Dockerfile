FROM python:3.10.4-bullseye
WORKDIR /Bot
COPY Pipfile ./ /Bot/
COPY Pipfile.lock ./ /Bot/
RUN pip install --upgrade pip pipenv
RUN pipenv install
EXPOSE 4001
CMD ["pipenv", "run", "python", "./Bot/rinbot.py"]