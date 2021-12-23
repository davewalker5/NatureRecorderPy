FROM python:3.10-slim-bullseye AS runtime

COPY naturerecorderpy-1.0.6.0 /opt/naturerecorderpy-1.0.6.0

WORKDIR /opt/naturerecorderpy-1.0.6.0

RUN apt-get update -y
RUN pip install -r requirements.txt
RUN pip install nature_recorder-1.0.6-py3-none-any.whl

ENV NATURE_RECORDER_DATA_FOLDER=/var/opt/naturerecorderpy-1.0.6.0
ENV NATURE_RECORDER_DB=/var/opt/naturerecorderpy-1.0.6.0/naturerecorder.db

ENTRYPOINT [ "python" ]
CMD [ "-m", "naturerec_web" ]
