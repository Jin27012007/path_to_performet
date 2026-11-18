#!/usr/bin/env bash
set -euo pipefail

export DISPLAY=:1
export QT_X11_NO_MITSHM=1

if ! pgrep -f "Xvfb :1" >/dev/null 2>&1; then
  Xvfb :1 -screen 0 1600x1000x24 -ac +extension GLX +render -noreset \
    >"$HOME/.xvfb.log" 2>&1 &
  sleep 2
fi

if ! pgrep -f "xfce4-session" >/dev/null 2>&1; then
  dbus-launch --exit-with-session startxfce4 >"$HOME/.xfce.log" 2>&1 &
  sleep 3
fi

if ! pgrep -f "x11vnc.*5900" >/dev/null 2>&1; then
  x11vnc -display :1 -forever -shared -nopw -listen 0.0.0.0 -rfbport 5900 \
    >"$HOME/.x11vnc.log" 2>&1 &
  sleep 1
fi

if ! pgrep -f "websockify.*6080" >/dev/null 2>&1; then
  websockify --web=/usr/share/novnc/ 0.0.0.0:6080 127.0.0.1:5900 \
    >"$HOME/.novnc.log" 2>&1 &
fi

echo "Desktop remoto pronto na porta encaminhada 6080."
