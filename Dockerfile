FROM python:3.11-slim

RUN apt update && apt install -y ffmpeg

WORKDIR /opt/tapo-downloader

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY main.py .

CMD [ "python", "./main.py" ]
