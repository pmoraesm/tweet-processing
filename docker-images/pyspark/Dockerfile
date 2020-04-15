FROM ubuntu:18.04

RUN mkdir /app

COPY ./loop.sh /app/ && \
     ./sample_tweet.json /app/ && \
     ./sample_tweet.json  /app/

RUN apt-get update -y && apt-get install -y \
    python3-pip \
    openjdk-8-jdk \
    wget

RUN echo 'alias python="/usr/bin/python3"' >> /root/.bashrc && \
    echo 'alias pip="/usr/bin/pip3"' >> /root/.bashrc && \
    echo 'export PYSPARK_PYTHON="/usr/bin/python3"' >> /root/.bashrc && \
    echo 'export PYTHONIOENCODING=utf8' >> /root/.bashrc && \
    chmod 755 /app/loop.sh

RUN /usr/bin/python3 -m pip install pyspark

CMD /app/loop.sh

