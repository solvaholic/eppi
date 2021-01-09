#/bin/bash
# Listen on UDP 34567; Pipe output to ./eprint.py

cd ~/repos/eppi

while true; do
  printf "Waiting for input on UDP port 34567...\n"
  nc -u -l 0.0.0.0 34567 -w0 | ./eprint.py
  printf "Pausing...\n"
  sleep 10
done

# Send a message to this listener:
#   echo "YourMessageHere" | nc -u HOST 34567 -w0
