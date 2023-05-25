#!/bin/sh

export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:$pwd


./DCA1000EVM_CLI_Control fpga configFile.json 


./DCA1000EVM_CLI_Control record configFile.json 

./DCA1000EVM_CLI_Control start_record configFile.json -q 


echo Conf Ok



