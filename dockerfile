FROM python:3.9.6
WORKDIR /Bot
COPY . .
RUN pip install discord==1.7.3
RUN pip install python-dotenv==0.19.0
ENTRYPOINT ["python"]
