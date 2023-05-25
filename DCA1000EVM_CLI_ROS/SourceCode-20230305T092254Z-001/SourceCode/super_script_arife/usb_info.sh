#!/bin/bash
lsusb
echo 
echo 


gnome-terminal -- bash -c "ll /dev/serial/by-id;exec bash"
echo ENV is ok

