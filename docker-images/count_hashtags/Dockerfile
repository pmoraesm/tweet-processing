FROM ubuntu:18.04

ENV PYSPARK_PYTHON="/usr/bin/python3"
ENV PYSPARK_PYTHON="/usr/bin/python3"

RUN apt-get update -y && apt-get install -y \
    python3-pip \
    openjdk-8-jdk

RUN mkdir /home/app/ \
    && chmod -R 755 /home/app/ \
    && /usr/bin/python3 -m pip install pyspark

COPY ./count_hashtags.py ./start.sh ./sample_tweet.json /home/app/

CMD ["/home/app/start.sh"]

