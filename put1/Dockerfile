FROM nikolaik/python-nodejs:python3.10-nodejs18

RUN apt-get update -y && apt-get upgrade -y \
    && apt-get install -y --no-install-recommends ffmpeg neofetch \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app/
COPY . /app/

RUN pip3 install -U -r req*

CMD ["python3", "-m", "ubot"]