FROM selenium/standalone-firefox:latest as build

RUN sudo apt-get update && sudo apt-get upgrade -y && \
    sudo apt-get install vim python3-pip -y

COPY geckodriver_linux /usr/local/bin

RUN pip install selenium pyvirtualdisplay numpy

FROM build

WORKDIR /home/seluser

COPY *.py /home/seluser
