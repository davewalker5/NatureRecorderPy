FROM python:3.10-slim-bullseye AS runtime

COPY naturerecorderpy-1.7.0.0 /opt/naturerecorderpy

WORKDIR /opt/naturerecorderpy

RUN apt-get update -y
RUN pip install -r requirements.txt
RUN pip install nature_recorder-1.7.0-py3-none-any.whl

ENV NATURE_RECORDER_DATA_FOLDER=/var/opt/naturerecorderpy
ENV NATURE_RECORDER_DB=/var/opt/naturerecorderpy/naturerecorder.db

ENTRYPOINT [ "python" ]
CMD [ "-m", "naturerec_web", "production" ]
