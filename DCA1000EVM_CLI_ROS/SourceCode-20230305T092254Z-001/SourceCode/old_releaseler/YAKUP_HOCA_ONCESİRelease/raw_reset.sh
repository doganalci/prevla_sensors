
export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:$pwd

./DCA1000EVM_CLI_Control fpga configFile.json



./DCA1000EVM_CLI_Control reset_ar_device configFile.json
