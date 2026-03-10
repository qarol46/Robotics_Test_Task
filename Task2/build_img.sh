#!/bin/bash

# Получаем аргумент (по умолчанию osrf/ros:humble-desktop-full, еще tiryoh/ros2-desktop-vnc:humble-arm64-20230129T1546)
BASE_IMAGE=${1:-osrf/ros:humble-desktop-full}

docker build --build-arg BASE_IMAGE="$BASE_IMAGE" -t wheeled .
