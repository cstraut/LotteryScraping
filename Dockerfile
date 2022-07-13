FROM selenium/standalone-firefox:latest as build

RUN apt-get -qay update && apt-get -qay upgrade && \
    apt-get install vim -y

COPY geckodriver_linux /usr/local/bin

FROM build

WORKDIR /usr/src/app

COPY *.py /usr/src/app/
