FROM python:3.10-slim-buster

WORKDIR /app

RUN /usr/local/bin/python -m pip install --upgrade pip
RUN pip3 install requests

COPY /src .

ENTRYPOINT [ "python3", "/app/main.py"]
