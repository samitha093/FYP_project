# FROM ubuntu:20.04
FROM python:3

RUN pip install aiohttp

WORKDIR /app
COPY ./ ./

COPY startup.sh .
RUN chmod +x startup.sh

CMD ["./startup.sh"]

