# whisper-api
Simple API for Whisper

## Installation

	pip install -r requirements.txt

Make sure you have GPU acceleration configured and turned on.

## Run

    docker build --build-arg MODEL=small -t whisper-api .
    docker run -p 8000:8000 -t whisper-api

## Usage

/GET /status

Find out service is on and GPU is available

/POST /transcribe

:file: File to upload

:start: Where to start transcribing audio in minutes, optional

:end: Where to end transcribing audio in minutes, optional
