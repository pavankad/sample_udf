FROM ubuntu:20.04
RUN apt-get -y update && apt-get -y upgrade && apt-get install -y software-properties-common
RUN add-apt-repository -y ppa:deadsnakes/ppa && apt-get -y update
RUN apt-get install -y python3.11 
RUN update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.11 1
RUN apt-get install -y protobuf-compiler python3-dev patchelf