#!/bin/bash

function log-preamble {
  echo "=== Setting up log files... ==="
  if [ -d "/var/log" ]; then {
    touch /var/log/orionrexec.log
    chmod +w /var/log/orionrexec.log
  } fi
}

function log-body {
  if [ ! -d "/var/log" ]; then {
    read -p "Where are logs stored on your system? --> " dir
    touch $dir/orionrexec.log
    chmod +w $dir/orionrexec.log
  } fi
}

function file-setup {
  echo "=== Setting permissions... ==="
  chmod +x server.py
  echo "=== Setting up configuration files... ==="
  mkdir /etc/orion
  touch /etc/orion/orion.conf
}

function main {
  log-preamble
  log-body
  file-setup
}

main
