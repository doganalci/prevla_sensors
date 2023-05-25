#!/bin/sh


echo Killing starts

kill -9 $(ps aux | grep 'DCA1000EVM_CLI_Record' | awk '{print $2}')



echo  Running Process Killed



