FROM nvidia/cuda:11.2.2-cudnn8-devel-ubuntu20.04

ARG PROJECT_NAME=asr
ARG MODEL=small

ENV MODEL=$MODEL

RUN apt update \
    && DEBIAN_FRONTEND=noninteractive apt install -y tzdata \
    && apt install -y software-properties-common \
    && add-apt-repository -y ppa:deadsnakes/ppa \
    && apt update \
    && apt install -y python3-pip \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /root/$PROJECT_NAME

ADD requirements.txt .
RUN pip install -r requirements.txt

COPY . .

RUN chmod a+x run_script.sh

EXPOSE 8000

CMD ["./run_script.sh"]
