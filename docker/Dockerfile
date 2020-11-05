FROM continuumio/anaconda3
MAINTAINER byeongho.kang@yahoo.com

WORKDIR /
COPY filesystem.tar .
RUN tar xf filesystem.tar

WORKDIR /root

RUN apt update
RUN apt upgrade -y
RUN apt install
RUN apt install -y openssh-server vim
RUN service ssh start

RUN git clone https://github.com/streamreturns/heimdall.git
RUN pip install -r heimdall/requirements.txt

RUN echo "FASTAPI KR" > /root/heimdall/config/stage_identifier

EXPOSE 22