#!/bin/bash
LOG_FILE="$HOME/LeadSmithOS/boot.log"
FAIL_COUNT_FILE="$HOME/LeadSmithOS/.fail_count"
if [ ! -f $FAIL_COUNT_FILE ]; then echo 0 > $FAIL_COUNT_FILE; fi
COUNT=$(cat $FAIL_COUNT_FILE)
if [ $COUNT -ge 3 ]; then
    echo "--- LEADSMITH OS: SAFE MODE ---"
    exit 1
fi
echo $((COUNT + 1)) > $FAIL_COUNT_FILE
python3 $HOME/LeadSmithOS/ls_dash.py
if [ $? -eq 0 ]; then echo 0 > $FAIL_COUNT_FILE; fi
