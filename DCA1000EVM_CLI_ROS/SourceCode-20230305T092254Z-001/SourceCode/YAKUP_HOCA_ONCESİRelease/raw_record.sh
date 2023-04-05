#!/bin/sh

export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:$pwd

echo yeah 1


./DCA1000EVM_CLI_Control fpga configFile.json

./DCA1000EVM_CLI_Control record configFile.json


echo Conf Ok



