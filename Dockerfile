<<<<<<< HEAD
FROM python:3.10.0
WORKDIR /Bot
COPY Pipfile ./ /Bot/
COPY Pipfile.lock ./ /Bot/
RUN pip install --upgrade pip pipenv
RUN pipenv install
CMD ["pipenv", "run", "python", "./Bot/kumikobot.py"]
=======
FROM python:3.10.1
WORKDIR /Bot
COPY Pipfile ./ /Bot/
COPY Pipfile.lock ./ /Bot/
COPY /Bot/Cogs/daTokens/tokens.db /Bot/Cogs/daTokens /Bot/Cogs/daTokens/
RUN pip install --upgrade pip pipenv
RUN pipenv install
CMD ["pipenv", "run", "python", "./Bot/rinbot.py"]
>>>>>>> a5659c14a6103770ed114e62aee8a13b58a89b5d
