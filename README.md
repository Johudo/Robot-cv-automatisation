# Robot automatisation using OpenCV
```
docker run --name robot_container  --device="/dev/video0:/dev/video0" -t -d johudo/storage-automatisation-robot:v1.0.1
docker start robot_container
docker exec -it robot_container bash
```
