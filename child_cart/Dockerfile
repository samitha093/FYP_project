FROM python:3.8

WORKDIR /app
COPY ./ ./

RUN apt-get update
RUN --mount=type=cache,target=/root/.cache/pip apt-get install -y libgl1-mesa-glx
RUN --mount=type=cache,target=/root/.cache/pip python -m pip install --upgrade pip
RUN --mount=type=cache,target=/root/.cache/pip pip install tensorflow_cpu-2.11.0-cp38-cp38-manylinux_2_17_x86_64.manylinux2014_x86_64.whl
COPY requirements.txt .
RUN --mount=type=cache,target=/root/.cache/pip pip install -r requirements.txt

COPY startup.sh .
RUN chmod +x startup.sh

CMD ["./startup.sh"]