# Используйте ваш базовый образ
ARG BASE_IMAGE
FROM ${BASE_IMAGE}

# Установите переменные окружения
ENV NVIDIA_VISIBLE_DEVICES=all
ENV NVIDIA_DRIVER_CAPABILITIES=compute,utility
ENV ROS_DISTRO=humble

# Установите ROS-пакеты и другие зависимости
RUN apt-get update && apt-get install -y \
    ros-${ROS_DISTRO}-rclcpp \
    ros-${ROS_DISTRO}-tf2 \
    ros-${ROS_DISTRO}-rclpy \
    ros-${ROS_DISTRO}-ros2-control \
    ros-${ROS_DISTRO}-tf-transformations \
    libasio-dev \
    gazebo \
    libgazebo-dev \
    ros-${ROS_DISTRO}-gazebo-ros \
    ros-${ROS_DISTRO}-gazebo-ros-pkgs \
    ros-${ROS_DISTRO}-gazebo-msgs \
    ros-${ROS_DISTRO}-gazebo-plugins \
    ros-${ROS_DISTRO}-velodyne-pointcloud \
    ros-${ROS_DISTRO}-velodyne \
    ros-${ROS_DISTRO}-velodyne-description \
    ros-${ROS_DISTRO}-velodyne-driver \
    ros-${ROS_DISTRO}-velodyne-gazebo-plugins \
    ros-${ROS_DISTRO}-velodyne-laserscan \
    ros-${ROS_DISTRO}-velodyne-msgs \
    ros-${ROS_DISTRO}-realsense2-description \
    ros-${ROS_DISTRO}-velodyne-simulator \
    ros-${ROS_DISTRO}-twist-mux \
    ros-${ROS_DISTRO}-pointcloud-to-laserscan \
    ros-${ROS_DISTRO}-graph-msgs \
    ros-${ROS_DISTRO}-moveit-core \        
    ros-${ROS_DISTRO}-moveit-ros \          
    ros-${ROS_DISTRO}-moveit-planners \      
    ros-${ROS_DISTRO}-moveit-kinematics \    
    ros-${ROS_DISTRO}-moveit-msgs \          
    ros-${ROS_DISTRO}-moveit-visual-tools \
    ros-${ROS_DISTRO}-ros2-controllers \      
    ros-${ROS_DISTRO}-controller-manager \    
    ros-${ROS_DISTRO}-diff-drive-controller \ 
    ros-${ROS_DISTRO}-gazebo-ros2-control \
    ros-${ROS_DISTRO}-robot-localization \ 
    ros-${ROS_DISTRO}-navigation2 \           
    ros-${ROS_DISTRO}-nav2-bringup \         
    ros-${ROS_DISTRO}-nav2-rviz-plugins \     
    ros-${ROS_DISTRO}-nav2-common \           
    ros-${ROS_DISTRO}-imu-filter-madgwick \   
    ros-${ROS_DISTRO}-slam-toolbox \          
    ros-${ROS_DISTRO}-rtabmap-ros \ 
    python3-kivy \
    iperf3 \
    nano \
    python3-pip \          
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*
    
# Установите Python-пакеты
RUN pip3 install zmq transforms3d

RUN apt-get update && apt-get upgrade -y && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*
    
RUN apt-get update && apt-get install -y \
    ros-${ROS_DISTRO}-perception-pcl \
    ros-${ROS_DISTRO}-pcl-msgs \
    ros-${ROS_DISTRO}-vision-opencv \
    ros-${ROS_DISTRO}-xacro \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

RUN apt-get update && apt-get install -y \
    software-properties-common \
    && add-apt-repository ppa:borglab/gtsam-release-4.1 -y \
    && apt-get update && apt-get install -y \
    libgtsam-dev \
    libgtsam-unstable-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

RUN apt-get update && apt-get install -y \
    cmake \
    build-essential \
    libboost-all-dev \
    libtbb-dev \
    python3-colcon-common-extensions \
    python3-rosdep \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*
    
# Установите рабочую директорию
WORKDIR /wheeled

# Скопируйте ваш код или ROS 2 workspace в образ (при необходимости)
COPY src/ /wheeled/src/

# Скопируйте файл cyclonedds.xml в образ
#COPY cyclonedds.xml /wheeled/cyclonedds.xml

# Установите переменные окружения для Cyclone DDS
#ENV RMW_IMPLEMENTATION=rmw_cyclonedds_cpp
#ENV CYCLONEDDS_URI=file:///wheeled/cyclonedds.xml

# (Опционально) Скопируйте скрипт запуска
# COPY entrypoint.sh /entrypoint.sh
# RUN chmod +x /entrypoint.sh

# Установите точку входа (entrypoint) или команду запуска
# ENTRYPOINT ["/entrypoint.sh"]
ENTRYPOINT ["/bin/bash"]
