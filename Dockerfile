FROM python:3.8-alpine
COPY ./ /app
RUN apk update
RUN apk add make automake gcc g++ subversion python3-dev
RUN pip3 install --upgrade pip3 setuptools wheel
RUN pip3 install -r /app/requirements.txt --no-cache-dir
RUN pip3 install -e /app
EXPOSE 8080
CMD web_server
