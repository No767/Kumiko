FROM python:3.10.1
WORKDIR /Bot
COPY Pipfile ./ /Bot/
COPY Pipfile.lock ./ /Bot/
COPY /Bot/Cogs/daTokens/tokens.db /Bot/Cogs/daTokens /Bot/Cogs/daTokens/
RUN pip install --upgrade pip pipenv
RUN pipenv install
EXPOSE 4001
CMD ["pipenv", "run", "python", "./Bot/rinbot.py"]