PORT=8080

all:
  install
  execbg

execbg:
  python3 src/server.py $(PORT) &

exec:
  python3 src/server.py $(PORT)

install:
  bash scripts/init.sh
