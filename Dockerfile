FROM nvidia/cuda:11.2.2-cudnn8-devel-ubuntu20.04

ARG PROJECT_NAME=asr
ARG MODEL=small

ENV MODEL=$MODEL

WORKDIR /root/$PROJECT_NAME

ADD requirements.txt .

RUN pip install -r requirements.txt \
    && chmod a+x run_script.sh

EXPOSE 50051

CMD ["run_script.sh"]
