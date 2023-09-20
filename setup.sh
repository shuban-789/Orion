#!/bin/bash

echo "=== Setting up log files... ==="
if [ -d "/var/log" ]; then
  touch /var/log/orionrexec.log
  chmod +w /var/log/orionrexec.log
fi
if [ ! -d "/var/log" ]; then
  read -p "Where are logs stored on your system? -> " dir
  touch $dir/orionrexec.log
  chmod +w $dir/orionrexec.log
echo "=== Setting permissions... ==="
chmod +x server.py
echo "=== Setting up configuration files... ==="
mkdir /etc/orion
touch /etc/orion/orion.conf
