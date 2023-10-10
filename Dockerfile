# Use an official Python runtime as a parent image
FROM python:3.8.17-slim

# Set environment variables
ENV QT_QPA_PLATFORM=wayland
ENV DEBIAN_FRONTEND=noninteractive

# Update apt database
RUN apt-get update && \
    apt-get upgrade -y && \
    apt-get install -y \
    apt-utils \
    software-properties-common \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Add mirrors for Gstreamer and Qt
RUN add-apt-repository main -y && add-apt-repository universe -y && add-apt-repository restricted -y && add-apt-repository multiverse -y


# Update and install required packages
RUN apt-get update && \
    apt-get upgrade -y && \
    apt-get install -y \
    qtmultimedia5-dev \
    libqt5multimedia5-plugins \
    wget \
    python3-dev \
    libxext-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Install SIP and PyQt5
RUN pip install --upgrade setuptools && \
    pip install sip && \
    pip install pyqt5 --config-settings --confirm-license= --verbose

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install Gstreamer
WORKDIR /app/gstreamer-1.16.0
RUN apt-get install flex 
RUN apt-get install bison
RUN pip install meson
RUN mdir build
RUN meson build -Dintrospection=disabled 
WORKDIR /app/gstreamer-1.16.0/build
RUN ninja
RUN ninja install

# Install Gstreamer plugins
RUN apt-get install libgstreamer1.0-dev libgstreamer-plugins-base1.0-dev libgstreamer-plugins-bad1.0-dev gstreamer1.0-plugins-base gstreamer1.0-plugins-good gstreamer1.0-plugins-bad gstreamer1.0-plugins-ugly gstreamer1.0-libav gstreamer1.0-tools gstreamer1.0-x gstreamer1.0-alsa gstreamer1.0-gl gstreamer1.0-gtk3 gstreamer1.0-qt5 gstreamer1.0-pulseaudio

# Install Gstreamer Python bindings
RUN pip install pygobject pycairo PyGObject 
RUN git clone https://github.com/GStreamer/gst-python.git
WORKDIR /app/gst-python

# Build Gstreamer Python bindings
RUN export PYTHON=/usr/bin/python3
RUN git checkout 1.19.2
RUN mkdir build
WORKDIR /app/gst-python/build
RUN meson build -Dintrospection=disabled
RUN ninja
RUN ninja install