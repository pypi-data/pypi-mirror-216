#!/bin/bash

# Run the IP Address Command and assign the output to a variable
output=$(ip -a -c -h addr | grep inet | grep enp | cut -d " " -f 6)

# Extract the IP address prefix without additional digits or subnet mask
check=$(echo "$output" | grep -o "10.10.40")

# Test
#echo "$output" 
#echo "$check"

# If statements to check if IP address is properly configured
if [ "$check" != "10.10.40" ]; then
    echo "Error: Your IP address is not properly configured." 
    echo "Set your Wired IPv4 address to any value from 10.10.40.XXX except 10.10.40.201" 
else
    echo "Your Wired IP address is configured properly" 
fi
