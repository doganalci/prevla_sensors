#!/bin/sh
export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:$pwd
rm temp.csv
./DCA1000EVM_CLI_Control fpga configFile.json
./DCA1000EVM_CLI_Control stop_record configFile.json 


./DCA1000EVM_CLI_Control reset_ar_device configFile.json
ps -ef | grep "DCA" | awk '{print $2}' >> temp.csv
kill -9 $(awk -F"," 'FNR==1 {print $1}' temp.csv)
#./DCA1000EVM_CLI_Control stop_record configFile.json 
echo [INFO_Doga] KILL OK

