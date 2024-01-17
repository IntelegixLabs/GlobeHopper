FROM python:3.10.13-slim
LABEL maintainer="Subhransu <subhransud525@gmail.com>"

RUN apt-get update && apt-get install -y libgl1-mesa-glx libglib2.0-0 ffmpeg
RUN pip install ffmpeg-downloader
RUN pip install ffprobe
RUN apt-get update & apt-get install sqlite3
RUN pip install pysqlite3-binary

COPY ./requirements.txt /requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

RUN mkdir -p /app
COPY . /app
WORKDIR /app/

EXPOSE 5000

CMD ["/usr/bin/supervisord"]
CMD ["python", "app.py"]
ENV PYTHONBUFFERED 1
