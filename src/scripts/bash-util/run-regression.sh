#!/bin/bash

python3 -u src/scripts/regression-model/regression_model.py \
	--start-year 1964 --gdp-avg --gdp-log --pop-avg --pop-log --sep-host \
	--log -v --save \
	--reg-zinb --reg-hc0 \
	--ctrl-vars GDP POP AM HOST PRE POST YEAR COMM &

#python3 -u src/scripts/regression-model/regression_model.py \
#	--start-year 1996 --gdp-avg --gdp-log --pop-avg --pop-log --sep-host \
#	--log -v --save \
#	--reg-zinb --reg-hc3 \
#	--ctrl-vars GDP POP AM HOST PRE POST YEAR COMM &

wait
