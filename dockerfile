FROM python:3.10-rc-slim
WORKDIR /Bot
COPY requirements.txt ./Bot
RUN python -m pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt
CMD ["python", "./rinbot.py"]
