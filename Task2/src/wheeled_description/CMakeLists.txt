cmake_minimum_required(VERSION 3.5)
project(wheeled_description)

# Default to C99
if(NOT CMAKE_C_STANDARD)
  set(CMAKE_C_STANDARD 99)
endif()

# Default to C++14
if(NOT CMAKE_CXX_STANDARD)
  set(CMAKE_CXX_STANDARD 14)
endif()

if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  add_compile_options(-Wall -Wextra -Wpedantic)
endif()

find_package(ament_cmake REQUIRED)
find_package(rclcpp REQUIRED)
find_package(rclpy REQUIRED)

# Основные сообщения ROS2
find_package(std_msgs REQUIRED)
find_package(sensor_msgs REQUIRED)
find_package(geometry_msgs REQUIRED)
find_package(nav_msgs REQUIRED)
find_package(std_srvs REQUIRED)

# TF зависимости
find_package(tf2_ros REQUIRED)
find_package(tf2 REQUIRED)
find_package(tf2_msgs REQUIRED)
find_package(tf2_eigen REQUIRED)
find_package(tf2_geometry_msgs REQUIRED)
find_package(tf2_sensor_msgs REQUIRED)

# Gazebo и управление
find_package(robot_state_publisher REQUIRED)
find_package(xacro REQUIRED)
find_package(ros2_control REQUIRED)
find_package(ros2_controllers REQUIRED)
find_package(gazebo_ros2_control REQUIRED)

# PCL и математические библиотеки
find_package(PCL 1.10 REQUIRED COMPONENTS common io filters registration)
find_package(Eigen3 REQUIRED)
find_package(TBB REQUIRED)
find_package(pcl_conversions REQUIRED)

# YAML
find_package(yaml-cpp REQUIRED)

if(NOT PCL_FOUND)
    message(FATAL_ERROR "PCL not found. Please install libpcl-dev")
endif()

if(NOT Eigen3_FOUND)
    message(FATAL_ERROR "Eigen3 not found. Please install libeigen3-dev")
endif()

include_directories(
  include
  ${PCL_INCLUDE_DIRS}
  ${Eigen3_INCLUDE_DIR}
)

ament_export_dependencies(
  rclcpp
  rclpy
  std_msgs
  sensor_msgs
  geometry_msgs
  nav_msgs
  std_srvs
  tf2_ros
  tf2
  tf2_msgs
  tf2_eigen
  tf2_geometry_msgs
  tf2_sensor_msgs
  robot_state_publisher
  xacro
  ros2_control
  ros2_controllers
  gazebo_ros2_control
  nav2_bringup
  navigation2
  nav2_msgs
  slam_toolbox
)

install(
  DIRECTORY config launch meshes urdf worlds
  DESTINATION share/${PROJECT_NAME}
)

if(BUILD_TESTING)
  find_package(ament_lint_auto REQUIRED)
  set(ament_cmake_cpplint_FOUND TRUE)
  ament_lint_auto_find_test_dependencies()
endif()

ament_package()