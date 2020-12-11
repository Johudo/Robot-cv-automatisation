FROM jjanzic/docker-python3-opencv

COPY ./ /app

RUN pip install --upgrade pip setuptools wheel
RUN pip install -r /app/requirements.txt --no-cache-dir

RUN wget -P /app/src/yolo_files/ https://pjreddie.com/media/files/yolov3.weights

# EXPOSE 8080
# CMD web_server

