FROM mcr.microsoft.com/devcontainers/cpp:ubuntu-24.04

ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential git make pkg-config \
    qt6-base-dev qt6-declarative-dev qt6-charts-dev qt6-tools-dev qt6-tools-dev-tools qt6-svg-dev qmake6 qt6-qmake \
    xfce4 xfce4-terminal dbus-x11 xauth x11-xserver-utils \
    xvfb x11vnc novnc websockify \
    fonts-dejavu-core ca-certificates curl \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

ENV DISPLAY=:1
