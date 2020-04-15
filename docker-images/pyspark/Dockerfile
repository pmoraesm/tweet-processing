FROM ubuntu:18.04

RUN mkdir /home/app/

COPY ./loop.sh ./sample_tweet.json /home/app/


RUN apt-get update -y && apt-get install -y \
    python3-pip \
    openjdk-8-jdk \
    wget

RUN echo 'alias python="/usr/bin/python3"' >> /root/.bashrc && \
    echo 'alias pip="/usr/bin/pip3"' >> /root/.bashrc && \
    echo 'export PYSPARK_PYTHON="/usr/bin/python3"' >> /root/.bashrc && \
    echo 'export PYTHONIOENCODING=utf8' >> /root/.bashrc && \
    chmod 755 /home/app/loop.sh

RUN /usr/bin/python3 -m pip install pyspark

CMD /home/app/loop.sh