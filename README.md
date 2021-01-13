# Robot automatisation using OpenCV

To start docker container:

```bash
docker run \
    --name robot_container \
    --device=/dev/video0:/dev/video0 \
    -e DISPLAY=$DISPLAY \
    -t -d johudo/storage-automatisation-robot:v1.0.1
```

To start application:

```bash
xhost local:root
docker exec -it robot_container bash

# In container console
python /app/src/app.py
```

