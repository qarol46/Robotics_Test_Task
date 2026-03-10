#!/bin/sh

CONTAINER_NAME="wheeled"  
COMMANDS=". install/setup.bash"  

docker exec -it "$CONTAINER_NAME" /bin/bash -c "$COMMANDS && exec /bin/bash"
