FROM python:3.10.1
LABEL org.opencontainers.image.source="https://github.com/No767/Kumiko-Hub"
WORKDIR /Bot
COPY Pipfile ./ /Bot/
COPY Pipfile.lock ./ /Bot/
RUN pip install --upgrade pip pipenv
RUN pipenv install
EXPOSE 4002
CMD ["pipenv", "run", "python", "./Bot/kumikobot.py"]
