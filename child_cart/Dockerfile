# FROM ubuntu:20.04
FROM python:3.7.3-stretch

WORKDIR /app
COPY ./ ./

RUN python -m pip install --upgrade pip
COPY requirements.txt .
RUN --mount=type=cache,target=/root/.cache/pip pip install -r requirements.txt

COPY startup.sh .
RUN chmod +x startup.sh

CMD ["./startup.sh"]

