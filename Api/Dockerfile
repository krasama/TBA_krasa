FROM python:3.8-slim-buster

WORKDIR /app

COPY ./app .

COPY requirements.txt .

RUN pip3 install -r requirements.txt

EXPOSE 5000

CMD ["python","./app.py"]
