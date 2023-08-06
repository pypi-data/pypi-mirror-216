#!/bin/bash
set -e

# Checks output of checkipcon script to see if computer is configured to continue
output=$(bash ../shell_scripts/checkipcon.sh)
echo "$output" 

# If it passes then run the checksdr script and pass it the parameters from the python script for the bandchange script
expected="Your Wired IP address is configured properly"
if [ "$output" == "$expected" ]; then

    ULEARFCN=$1
    DLEARFCN=$2
    BAND=$3
    BAND_WIDTH=$4


   
    sshpass -p 'D9!*3n4Fw7Ka' ssh root@10.10.40.201 -oHostKeyAlgorithms=+ssh-rsa -t 'bash checksdr.sh'
    sshpass -p 'D9!*3n4Fw7Ka' ssh root@10.10.40.201 -oHostKeyAlgorithms=+ssh-rsa -t "bash bandchange.sh $ULEARFCN $DLEARFCN $BAND $BAND_WIDTH"

    echo "Band Change is Successful" 
    else
    echo "Failure" 
fi
