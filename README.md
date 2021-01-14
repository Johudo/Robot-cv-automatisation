# Robot automatisation using OpenCV

## Start application

To start docker container:

```bash
docker run \
    --name robot_container \
    --device=/dev/video0:/dev/video0 \
    -e DISPLAY=$DISPLAY \
    -v /tmp/.X11-unix/:/tmp/.X11-unix
    -t -d johudo/storage-automatisation-robot:v1.0.2
```

To start application:

```bash
xhost +local:docker
docker exec -it robot_container bash

# In container console
python /app/src/app.py
```

## Testing application

To **test** application, get container's IP

```bash
docker inspect \
    -f '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' \
    containerID
```

And use this URLs to control:

```bash
# To start:
http://containerIP:5000/start

# To stop:
http://containerIP:5000/stop
```