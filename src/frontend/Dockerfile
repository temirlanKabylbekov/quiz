FROM node:6
WORKDIR /srv
ADD package.json /srv
RUN npm install
ADD . /srv
EXPOSE 8080
