FROM python:3.8

WORKDIR /app

COPY requirements.txt /app
RUN pip install -r requirements.txt

COPY /src /app

ENTRYPOINT [ "python", "main.py" ]