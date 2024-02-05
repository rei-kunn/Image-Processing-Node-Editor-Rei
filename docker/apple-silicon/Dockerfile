# FROM python:3.10
# FROM arm64v8/ubuntu:22.04

# Use Python 3.10 slim image based on Debian Bullseye
FROM python:3.10-slim-bullseye

ENV TZ=Asia/Tokyo
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone
ENV DEBIAN_FRONTEND=noninteractive

# # NVIDIA -------------------------------------------------------------
# ENV NVIDIA_VISIBLE_DEVICES ${NVIDIA_VISIBLE_DEVICES:-all}
# ENV NVIDIA_DRIVER_CAPABILITIES ${NVIDIA_DRIVER_CAPABILITIES:+$NVIDIA_DRIVER_CAPABILITIES,}graphics

# xserver ------------------------------------------------------------
RUN apt update && apt -y upgrade && \
apt install -y xserver-xorg && \
apt -y clean && \
rm -rf /var/lib/apt/lists/*

# Install Python and pip
RUN apt update && apt install -y python3 python3-pip

# PyPI environment ---------------------------------------------------
RUN pip3 install --upgrade pip

# For error avoidance
RUN pip3 install --upgrade cython numpy==1.23.5

# RUN pip3 install \
# opencv-contrib-python==4.5.5.64 \
# # onnxruntime-gpu==1.12.0 \
# onnxruntime>=1.12.0 \
# dearpygui>=1.9.0 \
# mediapipe>=0.8.10 \
# protobuf>=3.20.0 \
# filterpy>=1.4.5 \

RUN pip3 install opencv-contrib-python==4.5.5.64 onnxruntime>=1.12.0 mediapipe>=0.8.10 protobuf>=3.20.0 filterpy>=1.4.5
# dearpygui>=1.9.0
# # macos
# COPY dearpygui-1.11.0-cp311-cp311-macosx_11_0_arm64.whl /tmp/
# RUN pip3 install /tmp/dearpygui-1.11.0-cp311-cp311-macosx_11_0_arm64.whl

# linux
COPY dearpygui-1.11.0-cp310-cp310-manylinux1_x86_64.whl /tmp/
RUN pip3 install /tmp/dearpygui-1.11.0-cp311-cp311-macosx_11_0_arm64.whl

WORKDIR /workspace
CMD ["python3", "main.py"]
