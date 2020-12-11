FROM python:3.8-alpine
COPY ./ /app
RUN apk update
RUN apk add make automake gcc g++ libc-dev subversion python3-dev
# RUN pip3 install --upgrade setuptools wheel
RUN pip install --upgrade pip setuptools wheel
RUN pip install -r /app/requirements.txt --no-cache-dir
RUN pip install -e /app
# EXPOSE 8080
# CMD web_server
