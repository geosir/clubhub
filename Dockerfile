# Club Hub Dockerfile
FROM ubuntu:18.04

RUN ln -fs /usr/share/UTC /etc/localtime
ENV DEBIAN_FRONTEND noninteractive


RUN apt-get update -y && apt-get upgrade -y
RUN apt-get update -y && apt-get install -y curl
RUN apt-get update -y && apt-get install -y python3-pip
RUN apt-get update -y && apt-get install -y git

# There is a "yarn" in cmdtest which conflicts with the node yarn.
RUN apt-get remove -y cmdtest
RUN curl -sS https://dl.yarnpkg.com/debian/pubkey.gpg | apt-key add -
RUN echo "deb https://dl.yarnpkg.com/debian/ stable main" | tee /etc/apt/sources.list.d/yarn.list
RUN apt-get update -y && apt-get install -y yarn

RUN apt-get update -y && apt-get install -y apache2
RUN apt-get update -y && apt-get install -y libapache2-mod-wsgi-py3
RUN apt-get update -y && apt-get install -y postgresql postgresql-client libpq-dev

RUN ln -s `which nodejs` /usr/local/bin/node

RUN rm -rf /etc/apache2/sites-enabled/*
ADD clubhub.conf /etc/apache2/sites-enabled/
ADD clubhub/ /opt/clubhub
VOLUME /opt/media

WORKDIR /opt/clubhub

RUN yarn
RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt

CMD ["/bin/bash", "startserver.sh"]
