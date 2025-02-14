#!/bin/bash

# Start the first process
python3.8 ./bot.py -D
status=$?
if [ $status -ne 0 ]; then
  echo "Failed to start bot.py: $status"
  exit $status
fi

# Start the second process
./fetch_data.py -D
status=$?
if [ $status -ne 0 ]; then
  echo "Failed to start fetch_data.py: $status"
  exit $status
fi

while sleep 60; do
  ps aux |grep bot.py |grep -q -v grep
  PROCESS_1_STATUS=$?
  ps aux |grep fetch_data.py |grep -q -v grep
  PROCESS_2_STATUS=$?
  # If the greps above find anything, they exit with 0 status
  # If they are not both 0, then something is wrong
  if [ $PROCESS_1_STATUS -ne 0 -o $PROCESS_2_STATUS -ne 0 ]; then
    echo "One of the processes has already exited."
    exit 1
  fi
done

