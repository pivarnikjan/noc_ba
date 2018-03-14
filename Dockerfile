FROM python:3.6
MAINTAINER Jan Pivarnik <jp002f@intl.att.com>

ENV PYTHONUNBUFFERED 1

# creating directory, copying everything from host to container
ENV APP_DIR /opt/demo/
RUN mkdir ${APP_DIR}
WORKDIR ${APP_DIR}
COPY . ${APP_DIR}

# copying phantomjs binary inside container
ENV PHANTOM_JS phantomjs-2.1.1-linux-x86_64
RUN mv ${PHANTOM_JS} /usr/local/share && \
    ln -sf /usr/local/share/${PHANTOM_JS}/bin/phantomjs /usr/local/bin

# installing python dependencies
RUN pip3 install -r requirements.txt
# setting entrypoint directory
WORKDIR ${APP_DIR}/demo_nightofchances

# collecting changes in models and migrating this changes into DB
RUN ["python3", "manage.py", "makemigrations"]
RUN ["python3", "manage.py", "migrate"]

EXPOSE 8000

# running Django service
CMD ["python3", "manage.py", "runserver", "0:8000"]
