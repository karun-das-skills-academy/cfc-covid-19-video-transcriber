FROM registry.access.redhat.com/ubi8
WORKDIR /app
COPY Pipfile* /app/
USER root
RUN yum -y install python3
RUN yum -y install python3-pip wget
RUN pip3 install --upgrade pip \
  && pip3 install --upgrade pipenv \
  && pipenv install --system --deploy
RUN mkdir -p /app/server/audio_extractions
RUN mkdir -p /app/server/video_uploads
RUN mkdir -p /app/server/output_transcriptions
RUN mkdir -p /app/server/output_transcripts
# RUN mkdir -p /app/server/cfc-starter/audio_extractions
# RUN mkdir -p /app/server/cfc-starter/video_uploads

COPY . /app
# RUN chown -R :1024 /app
# RUN chown 1001 /app/server/audio_extractions
# RUN chown 1001 /app/server/video_uploads
# RUN chown 1001 /app/server/output_transcriptions
# RUN chown 1001 /cfc-covid-19-video-transcriber-starter/server/audio_extractions
# RUN chown 1001 /cfc-covid-19-video-transcriber-starter/server/video_uploads
# RUN chown 1001 /cfc-covid-19-video-transcriber-starter/server/output_transcripts

# RUN chmod -R 775 /app
# RUN chmod -R g+s /app

# RUN addgroup --gid 1024 mygroup
# RUN adduser --disabled-password --gecos "" --force-badname --ingroup 1024 myuser 
# USER myuser

# USER 1024

# RUN chmod 775 /app/server/audio_extractions
# RUN chmod 775 /app/server/video_uploads
# RUN chmod 775 /app/server/output_transcriptions
# RUN chmod 775 /cfc-covid-19-video-transcriber-starter/server/audio_extractions
# RUN chmod 775 /cfc-covid-19-video-transcriber-starter/server/video_uploads
# RUN chmod 775 /cfc-covid-19-video-transcriber-starter/server/output_transcripts

# COPY . /app

ENV FLASK_APP=server/__init__.py
CMD ["python3", "manage.py", "start", "0.0.0.0:3000"]

RUN useradd -u 1001 -g 0 ibm
RUN chown -R ibm /app && chmod -R 770 /app && chmod -R g+s /app
USER ibm
