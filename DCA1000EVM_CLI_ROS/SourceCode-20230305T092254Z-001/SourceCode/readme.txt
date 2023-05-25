rm -rf Release/ && make && cp super_script_arife/* Release && cd Release/


./raw_conf.sh && sleep 3 && ./raw_killer.sh && ./raw_stop.sh 


raw_conf.sh
Export+fpga+record+start

raw_killer.sh
kill -9 $(ps aux | grep 'DCA1000EVM_CLI_Record' | awk '{print $2}')



raw_stop.sh

export+fpga+stop






stop record error için timeout değerini dğüşür


