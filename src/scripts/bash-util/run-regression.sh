#!/bin/bash

python3 -u src/scripts/regression-model/regression_model.py \
	--start-year 1964 --gdp-avg --gdp-log --pop-avg --pop-log --sep-close \
	--log --save \
	--reg-zinb --reg-hc0 --max-lag 1 \
	--ctrl-vars GDP POP AM HOST PRE POST COMM CLOSE_CENTER CLOSE_GMT1 CLOSE_MAIN CLOSE_WEST CLOSE_WIDE &

#python3 -u src/scripts/regression-model/regression_model.py \
#	--start-year 1996 --gdp-avg --gdp-log --pop-avg --pop-log --sep-host \
#	--log -v --save \
#	--reg-zinb --reg-hc3 \
#	--ctrl-vars GDP POP AM HOST PRE POST YEAR COMM &

wait
