FROM python:3.9.6
WORKDIR /Bot
COPY . .
RUN pip install discord
RUN pip install python-dotenv
ENTRYPOINT ["python"]
