PORT=8080

all: execbg

execbg:
  python3 src/server.py $(PORT) &

exec:
  python3 src/server.py $(PORT)
