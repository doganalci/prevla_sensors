#!/bin/sh

export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:$pwd


./DCA1000EVM_CLI_Control stop_record configFile.json 


echo kapatildi
