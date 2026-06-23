FROM python:3.13-slim-bullseye AS runtime

ARG APP_VERSION
ARG RELEASE_VERSION

COPY naturerecorderpy-${RELEASE_VERSION} /opt/naturerecorderpy

WORKDIR /opt/naturerecorderpy

RUN apt-get update -y
RUN pip install nature_recorder-${APP_VERSION}-py3-none-any.whl

ENV NATURE_RECORDER_DATA_FOLDER=/var/opt/naturerecorderpy
ENV NATURE_RECORDER_DB=/var/opt/naturerecorderpy/naturerecorder.db

ENTRYPOINT [ "python" ]
CMD [ "-m", "naturerec_web", "production" ]
