FROM python:3.10.6-slim-bullseye
LABEL maintainer="Subhransu <subhransud525@gmail.com>"
RUN apt-get update && apt-get install -y libgl1-mesa-glx libglib2.0-0

COPY ./requirements.txt /requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

RUN mkdir -p /app
COPY . /app
WORKDIR /app/

CMD ["/usr/bin/supervisord"]
CMD ["python", "app.py"]
ENV PYTHONBUFFERED 1
