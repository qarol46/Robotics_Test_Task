#!/bin/bash

xhost +local:docker

docker run -it -e DISPLAY=$DISPLAY \
    --privileged \
    -v /tmp/.X11-unix:/tmp/.X11-unix \
    -e ROS_DOMAIN_ID=15 \
    --net host \
    --shm-size=6G \
    --volume $(pwd):/wheeled \
    -v /dev:/dev \
    -v $HOME/.gazebo/models:/root/.gazebo/models \
    --user root \
    --name wheeled wheeled \
    -c ". /opt/ros/humble/setup.bash; cd /wheeled; colcon build; . install/setup.bash; exec /bin/bash"

