FROM jjanzic/docker-python3-opencv

COPY ./ /app

# RUN apk update
# RUN apk add make automake gcc g++ libc-dev subversion python3-dev

RUN pip install --upgrade pip setuptools wheel
RUN pip install -r /app/requirements.txt --no-cache-dir
RUN pip install -e /app

# EXPOSE 8080
# CMD web_server
