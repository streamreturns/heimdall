FROM continuumio/anaconda3
MAINTAINER byeongho.kang@yahoo.com

WORKDIR /
COPY filesystem.tar.bz2 .
RUN tar xjf filesystem.tar.bz2

WORKDIR /root

RUN apt update
RUN apt upgrade -y
RUN apt install
RUN apt install -y openssh-server net-tools htop vim nano screen
RUN service ssh start

RUN git clone https://github.com/streamreturns/heimdall.git
RUN pip install -r heimdall/requirements.txt

RUN echo "FASTAPI KR" > /root/heimdall/config/stage_identifier

WORKDIR /root/heimdall

EXPOSE 22 65280-65407