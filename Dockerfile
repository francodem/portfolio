FROM alpine:latest

ADD . /app

WORKDIR /app

# Download, compile, and install Python
RUN apk add --upgrade --no-cache python3 py3-pip

RUN pip3 install --upgrade pip

RUN python3 -m venv /opt/env

ENV PATH="/opt/env/bin:$PATH"

ENV AWS_KEY=${AWS_KEY}

ENV AWS_SECRET_KEY=${AWS_SECRET_KEY}

ENV APP_SECRET_KEY=${APP_SECRET_KEY}

ENV SITE_KEY=${SITE_KEY}

ENV SERVER_KEY=${SERVER_KEY}

RUN pip3 install -r requirements.txt

EXPOSE 8080

CMD ["python3", "main.py"]