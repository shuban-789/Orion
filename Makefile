PORT=8080

all: exec

exec:
  python3 src/server.py $(PORT) &

stop:


