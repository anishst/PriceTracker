FROM python:alpine3.7
RUN apk add chromium
RUN apk add chromium-chromedriver
COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt
EXPOSE 5000
CMD python ./app.py
