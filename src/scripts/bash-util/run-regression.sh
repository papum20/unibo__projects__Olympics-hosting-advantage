#!/bin/bash

YEAR_START=1996
COV_TYPE=hc3
GDP_TYPE=log
POP_TYPE=log
REG_TYPE="--reg-zinb"


python3 -u src/scripts/regression-model/regression_model.py \
	--start-year ${YEAR_START} --gdp-avg --gdp-${GDP_TYPE} --pop-avg --pop-${POP_TYPE} \
	--log --save \
	${REG_TYPE} --reg-${COV_TYPE} --max-lag 1 \
	--ctrl-vars HOST AM YEAR &

python3 -u src/scripts/regression-model/regression_model.py \
	--start-year ${YEAR_START} --gdp-avg --gdp-${GDP_TYPE} --pop-avg --pop-${POP_TYPE} \
	--log --save \
	${REG_TYPE} --reg-${COV_TYPE} --max-lag 11 \
	--ctrl-vars HOST AM YEAR GDP POP COMM &


## SEP HOST

python3 -u src/scripts/regression-model/regression_model.py \
	--start-year ${YEAR_START} --gdp-avg --gdp-${GDP_TYPE} --pop-avg --pop-${POP_TYPE} --sep-host \
	--log --save \
	${REG_TYPE} --reg-${COV_TYPE} --max-lag 1 \
	--ctrl-vars HOST AM YEAR &

python3 -u src/scripts/regression-model/regression_model.py \
	--start-year ${YEAR_START} --gdp-avg --gdp-${GDP_TYPE} --pop-avg --pop-${POP_TYPE} --sep-host \
	--log --save \
	${REG_TYPE} --reg-${COV_TYPE} --max-lag 11 \
	--ctrl-vars HOST AM YEAR GDP POP COMM &


# PRE POST

python3 -u src/scripts/regression-model/regression_model.py \
	--start-year ${YEAR_START} --gdp-avg --gdp-${GDP_TYPE} --pop-avg --pop-${POP_TYPE} --sep-host \
	--log --save \
	${REG_TYPE} --reg-${COV_TYPE} --max-lag 1 \
	--ctrl-vars HOST AM YEAR PRE POST &

python3 -u src/scripts/regression-model/regression_model.py \
	--start-year ${YEAR_START} --gdp-avg --gdp-${GDP_TYPE} --pop-avg --pop-${POP_TYPE} --sep-host \
	--log --save \
	${REG_TYPE} --reg-${COV_TYPE} --max-lag 11 \
	--ctrl-vars HOST AM YEAR PRE POST GDP POP COMM &


# HOST, CLOSE

python3 -u src/scripts/regression-model/regression_model.py \
	--start-year ${YEAR_START} --gdp-avg --gdp-${GDP_TYPE} --pop-avg --pop-${POP_TYPE} \
	--log --save \
	${REG_TYPE} --reg-${COV_TYPE} --max-lag 11 \
	--ctrl-vars HOST AM YEAR PRE POST GDP POP COMM CLOSE_CENTER CLOSE_GMT1 CLOSE_MAIN CLOSE_WEST CLOSE_WIDE &

python3 -u src/scripts/regression-model/regression_model.py \
	--start-year ${YEAR_START} --gdp-avg --gdp-${GDP_TYPE} --pop-avg --pop-${POP_TYPE} --sep-host \
	--log --save \
	${REG_TYPE} --reg-${COV_TYPE} --max-lag 11 \
	--ctrl-vars HOST AM YEAR PRE POST GDP POP COMM CLOSE_CENTER CLOSE_GMT1 CLOSE_MAIN CLOSE_WEST CLOSE_WIDE &

python3 -u src/scripts/regression-model/regression_model.py \
	--start-year ${YEAR_START} --gdp-avg --gdp-${GDP_TYPE} --pop-avg --pop-${POP_TYPE} --sep-close \
	--log --save \
	${REG_TYPE} --reg-${COV_TYPE} --max-lag 11 \
	--ctrl-vars HOST AM YEAR PRE POST GDP POP COMM CLOSE_CENTER CLOSE_GMT1 CLOSE_MAIN CLOSE_WEST CLOSE_WIDE &

python3 -u src/scripts/regression-model/regression_model.py \
	--start-year ${YEAR_START} --gdp-avg --gdp-${GDP_TYPE} --pop-avg --pop-${POP_TYPE} --sep-host --sep-close \
	--log --save \
	${REG_TYPE} --reg-${COV_TYPE} --max-lag 11 \
	--ctrl-vars HOST AM YEAR PRE POST GDP POP COMM CLOSE_CENTER CLOSE_GMT1 CLOSE_MAIN CLOSE_WEST CLOSE_WIDE &


# HOST, CLOSE_GMT1

python3 -u src/scripts/regression-model/regression_model.py \
	--start-year ${YEAR_START} --gdp-avg --gdp-${GDP_TYPE} --pop-avg --pop-${POP_TYPE} \
	--log --save \
	${REG_TYPE} --reg-${COV_TYPE} --max-lag 11 \
	--ctrl-vars HOST AM YEAR PRE POST GDP POP COMM CLOSE_GMT1 &

python3 -u src/scripts/regression-model/regression_model.py \
	--start-year ${YEAR_START} --gdp-avg --gdp-${GDP_TYPE} --pop-avg --pop-${POP_TYPE} --sep-host \
	--log --save \
	${REG_TYPE} --reg-${COV_TYPE} --max-lag 11 \
	--ctrl-vars HOST AM YEAR PRE POST GDP POP COMM CLOSE_GMT1 &

python3 -u src/scripts/regression-model/regression_model.py \
	--start-year ${YEAR_START} --gdp-avg --gdp-${GDP_TYPE} --pop-avg --pop-${POP_TYPE} --sep-close \
	--log --save \
	${REG_TYPE} --reg-${COV_TYPE} --max-lag 11 \
	--ctrl-vars HOST AM YEAR PRE POST GDP POP COMM CLOSE_GMT1 &

python3 -u src/scripts/regression-model/regression_model.py \
	--start-year ${YEAR_START} --gdp-avg --gdp-${GDP_TYPE} --pop-avg --pop-${POP_TYPE} --sep-host --sep-close \
	--log --save \
	${REG_TYPE} --reg-${COV_TYPE} --max-lag 11 \
	--ctrl-vars HOST AM YEAR PRE POST GDP POP COMM CLOSE_GMT1 &


# HOST, CLOSE_WIDE

python3 -u src/scripts/regression-model/regression_model.py \
	--start-year ${YEAR_START} --gdp-avg --gdp-${GDP_TYPE} --pop-avg --pop-${POP_TYPE} \
	--log --save \
	${REG_TYPE} --reg-${COV_TYPE} --max-lag 11 \
	--ctrl-vars HOST AM YEAR PRE POST GDP POP COMM CLOSE_WIDE &

python3 -u src/scripts/regression-model/regression_model.py \
	--start-year ${YEAR_START} --gdp-avg --gdp-${GDP_TYPE} --pop-avg --pop-${POP_TYPE} --sep-host \
	--log --save \
	${REG_TYPE} --reg-${COV_TYPE} --max-lag 11 \
	--ctrl-vars HOST AM YEAR PRE POST GDP POP COMM CLOSE_WIDE &

python3 -u src/scripts/regression-model/regression_model.py \
	--start-year ${YEAR_START} --gdp-avg --gdp-${GDP_TYPE} --pop-avg --pop-${POP_TYPE} --sep-close \
	--log --save \
	${REG_TYPE} --reg-${COV_TYPE} --max-lag 11 \
	--ctrl-vars HOST AM YEAR PRE POST GDP POP COMM CLOSE_WIDE &

python3 -u src/scripts/regression-model/regression_model.py \
	--start-year ${YEAR_START} --gdp-avg --gdp-${GDP_TYPE} --pop-avg --pop-${POP_TYPE} --sep-host --sep-close \
	--log --save \
	${REG_TYPE} --reg-${COV_TYPE} --max-lag 11 \
	--ctrl-vars HOST AM YEAR PRE POST GDP POP COMM CLOSE_WIDE &





YEAR_START=1964
COV_TYPE=hc0


python3 -u src/scripts/regression-model/regression_model.py \
	--start-year ${YEAR_START} --gdp-avg --gdp-${GDP_TYPE} --pop-avg --pop-${POP_TYPE} \
	--log --save \
	${REG_TYPE} --reg-${COV_TYPE} --max-lag 1 \
	--ctrl-vars HOST AM YEAR &

python3 -u src/scripts/regression-model/regression_model.py \
	--start-year ${YEAR_START} --gdp-avg --gdp-${GDP_TYPE} --pop-avg --pop-${POP_TYPE} \
	--log --save \
	${REG_TYPE} --reg-${COV_TYPE} --max-lag 11 \
	--ctrl-vars HOST AM YEAR GDP POP COMM &


## SEP HOST

python3 -u src/scripts/regression-model/regression_model.py \
	--start-year ${YEAR_START} --gdp-avg --gdp-${GDP_TYPE} --pop-avg --pop-${POP_TYPE} --sep-host \
	--log --save \
	${REG_TYPE} --reg-${COV_TYPE} --max-lag 1 \
	--ctrl-vars HOST AM YEAR &

python3 -u src/scripts/regression-model/regression_model.py \
	--start-year ${YEAR_START} --gdp-avg --gdp-${GDP_TYPE} --pop-avg --pop-${POP_TYPE} --sep-host \
	--log --save \
	${REG_TYPE} --reg-${COV_TYPE} --max-lag 11 \
	--ctrl-vars HOST AM YEAR GDP POP COMM &


# PRE POST

python3 -u src/scripts/regression-model/regression_model.py \
	--start-year ${YEAR_START} --gdp-avg --gdp-${GDP_TYPE} --pop-avg --pop-${POP_TYPE} --sep-host \
	--log --save \
	${REG_TYPE} --reg-${COV_TYPE} --max-lag 1 \
	--ctrl-vars HOST AM YEAR PRE POST &

python3 -u src/scripts/regression-model/regression_model.py \
	--start-year ${YEAR_START} --gdp-avg --gdp-${GDP_TYPE} --pop-avg --pop-${POP_TYPE} --sep-host \
	--log --save \
	${REG_TYPE} --reg-${COV_TYPE} --max-lag 11 \
	--ctrl-vars HOST AM YEAR PRE POST GDP POP COMM &


# HOST, CLOSE

python3 -u src/scripts/regression-model/regression_model.py \
	--start-year ${YEAR_START} --gdp-avg --gdp-${GDP_TYPE} --pop-avg --pop-${POP_TYPE} \
	--log --save \
	${REG_TYPE} --reg-${COV_TYPE} --max-lag 11 \
	--ctrl-vars HOST AM YEAR PRE POST GDP POP COMM CLOSE_CENTER CLOSE_GMT1 CLOSE_MAIN CLOSE_WEST CLOSE_WIDE &

python3 -u src/scripts/regression-model/regression_model.py \
	--start-year ${YEAR_START} --gdp-avg --gdp-${GDP_TYPE} --pop-avg --pop-${POP_TYPE} --sep-host \
	--log --save \
	${REG_TYPE} --reg-${COV_TYPE} --max-lag 11 \
	--ctrl-vars HOST AM YEAR PRE POST GDP POP COMM CLOSE_CENTER CLOSE_GMT1 CLOSE_MAIN CLOSE_WEST CLOSE_WIDE &

python3 -u src/scripts/regression-model/regression_model.py \
	--start-year ${YEAR_START} --gdp-avg --gdp-${GDP_TYPE} --pop-avg --pop-${POP_TYPE} --sep-close \
	--log --save \
	${REG_TYPE} --reg-${COV_TYPE} --max-lag 11 \
	--ctrl-vars HOST AM YEAR PRE POST GDP POP COMM CLOSE_CENTER CLOSE_GMT1 CLOSE_MAIN CLOSE_WEST CLOSE_WIDE &

python3 -u src/scripts/regression-model/regression_model.py \
	--start-year ${YEAR_START} --gdp-avg --gdp-${GDP_TYPE} --pop-avg --pop-${POP_TYPE} --sep-host --sep-close \
	--log --save \
	${REG_TYPE} --reg-${COV_TYPE} --max-lag 11 \
	--ctrl-vars HOST AM YEAR PRE POST GDP POP COMM CLOSE_CENTER CLOSE_GMT1 CLOSE_MAIN CLOSE_WEST CLOSE_WIDE &


# HOST, CLOSE_GMT1

python3 -u src/scripts/regression-model/regression_model.py \
	--start-year ${YEAR_START} --gdp-avg --gdp-${GDP_TYPE} --pop-avg --pop-${POP_TYPE} \
	--log --save \
	${REG_TYPE} --reg-${COV_TYPE} --max-lag 11 \
	--ctrl-vars HOST AM YEAR PRE POST GDP POP COMM CLOSE_GMT1 &

python3 -u src/scripts/regression-model/regression_model.py \
	--start-year ${YEAR_START} --gdp-avg --gdp-${GDP_TYPE} --pop-avg --pop-${POP_TYPE} --sep-host \
	--log --save \
	${REG_TYPE} --reg-${COV_TYPE} --max-lag 11 \
	--ctrl-vars HOST AM YEAR PRE POST GDP POP COMM CLOSE_GMT1 &

python3 -u src/scripts/regression-model/regression_model.py \
	--start-year ${YEAR_START} --gdp-avg --gdp-${GDP_TYPE} --pop-avg --pop-${POP_TYPE} --sep-close \
	--log --save \
	${REG_TYPE} --reg-${COV_TYPE} --max-lag 11 \
	--ctrl-vars HOST AM YEAR PRE POST GDP POP COMM CLOSE_GMT1 &

python3 -u src/scripts/regression-model/regression_model.py \
	--start-year ${YEAR_START} --gdp-avg --gdp-${GDP_TYPE} --pop-avg --pop-${POP_TYPE} --sep-host --sep-close \
	--log --save \
	${REG_TYPE} --reg-${COV_TYPE} --max-lag 11 \
	--ctrl-vars HOST AM YEAR PRE POST GDP POP COMM CLOSE_GMT1 &


# HOST, CLOSE_WIDE

python3 -u src/scripts/regression-model/regression_model.py \
	--start-year ${YEAR_START} --gdp-avg --gdp-${GDP_TYPE} --pop-avg --pop-${POP_TYPE} \
	--log --save \
	${REG_TYPE} --reg-${COV_TYPE} --max-lag 11 \
	--ctrl-vars HOST AM YEAR PRE POST GDP POP COMM CLOSE_WIDE &

python3 -u src/scripts/regression-model/regression_model.py \
	--start-year ${YEAR_START} --gdp-avg --gdp-${GDP_TYPE} --pop-avg --pop-${POP_TYPE} --sep-host \
	--log --save \
	${REG_TYPE} --reg-${COV_TYPE} --max-lag 11 \
	--ctrl-vars HOST AM YEAR PRE POST GDP POP COMM CLOSE_WIDE &

python3 -u src/scripts/regression-model/regression_model.py \
	--start-year ${YEAR_START} --gdp-avg --gdp-${GDP_TYPE} --pop-avg --pop-${POP_TYPE} --sep-close \
	--log --save \
	${REG_TYPE} --reg-${COV_TYPE} --max-lag 11 \
	--ctrl-vars HOST AM YEAR PRE POST GDP POP COMM CLOSE_WIDE &

python3 -u src/scripts/regression-model/regression_model.py \
	--start-year ${YEAR_START} --gdp-avg --gdp-${GDP_TYPE} --pop-avg --pop-${POP_TYPE} --sep-host --sep-close \
	--log --save \
	${REG_TYPE} --reg-${COV_TYPE} --max-lag 11 \
	--ctrl-vars HOST AM YEAR PRE POST GDP POP COMM CLOSE_WIDE &





GDP_TYPE=logdiff
POP_TYPE=logdiff


python3 -u src/scripts/regression-model/regression_model.py \
	--start-year ${YEAR_START} --gdp-avg --gdp-${GDP_TYPE} --pop-avg --pop-${POP_TYPE} \
	--log --save \
	${REG_TYPE} --reg-${COV_TYPE} --max-lag 11 \
	--ctrl-vars HOST AM YEAR GDP POP COMM &


## SEP HOST

python3 -u src/scripts/regression-model/regression_model.py \
	--start-year ${YEAR_START} --gdp-avg --gdp-${GDP_TYPE} --pop-avg --pop-${POP_TYPE} --sep-host \
	--log --save \
	${REG_TYPE} --reg-${COV_TYPE} --max-lag 11 \
	--ctrl-vars HOST AM YEAR GDP POP COMM &


# PRE POST

python3 -u src/scripts/regression-model/regression_model.py \
	--start-year ${YEAR_START} --gdp-avg --gdp-${GDP_TYPE} --pop-avg --pop-${POP_TYPE} --sep-host \
	--log --save \
	${REG_TYPE} --reg-${COV_TYPE} --max-lag 11 \
	--ctrl-vars HOST AM YEAR PRE POST GDP POP COMM &


# HOST, CLOSE

python3 -u src/scripts/regression-model/regression_model.py \
	--start-year ${YEAR_START} --gdp-avg --gdp-${GDP_TYPE} --pop-avg --pop-${POP_TYPE} \
	--log --save \
	${REG_TYPE} --reg-${COV_TYPE} --max-lag 11 \
	--ctrl-vars HOST AM YEAR PRE POST GDP POP COMM CLOSE_CENTER CLOSE_GMT1 CLOSE_MAIN CLOSE_WEST CLOSE_WIDE &

python3 -u src/scripts/regression-model/regression_model.py \
	--start-year ${YEAR_START} --gdp-avg --gdp-${GDP_TYPE} --pop-avg --pop-${POP_TYPE} --sep-host \
	--log --save \
	${REG_TYPE} --reg-${COV_TYPE} --max-lag 11 \
	--ctrl-vars HOST AM YEAR PRE POST GDP POP COMM CLOSE_CENTER CLOSE_GMT1 CLOSE_MAIN CLOSE_WEST CLOSE_WIDE &

python3 -u src/scripts/regression-model/regression_model.py \
	--start-year ${YEAR_START} --gdp-avg --gdp-${GDP_TYPE} --pop-avg --pop-${POP_TYPE} --sep-close \
	--log --save \
	${REG_TYPE} --reg-${COV_TYPE} --max-lag 11 \
	--ctrl-vars HOST AM YEAR PRE POST GDP POP COMM CLOSE_CENTER CLOSE_GMT1 CLOSE_MAIN CLOSE_WEST CLOSE_WIDE &

python3 -u src/scripts/regression-model/regression_model.py \
	--start-year ${YEAR_START} --gdp-avg --gdp-${GDP_TYPE} --pop-avg --pop-${POP_TYPE} --sep-host --sep-close \
	--log --save \
	${REG_TYPE} --reg-${COV_TYPE} --max-lag 11 \
	--ctrl-vars HOST AM YEAR PRE POST GDP POP COMM CLOSE_CENTER CLOSE_GMT1 CLOSE_MAIN CLOSE_WEST CLOSE_WIDE &


# HOST, CLOSE_GMT1

python3 -u src/scripts/regression-model/regression_model.py \
	--start-year ${YEAR_START} --gdp-avg --gdp-${GDP_TYPE} --pop-avg --pop-${POP_TYPE} \
	--log --save \
	${REG_TYPE} --reg-${COV_TYPE} --max-lag 11 \
	--ctrl-vars HOST AM YEAR PRE POST GDP POP COMM CLOSE_GMT1 &

python3 -u src/scripts/regression-model/regression_model.py \
	--start-year ${YEAR_START} --gdp-avg --gdp-${GDP_TYPE} --pop-avg --pop-${POP_TYPE} --sep-host \
	--log --save \
	${REG_TYPE} --reg-${COV_TYPE} --max-lag 11 \
	--ctrl-vars HOST AM YEAR PRE POST GDP POP COMM CLOSE_GMT1 &

python3 -u src/scripts/regression-model/regression_model.py \
	--start-year ${YEAR_START} --gdp-avg --gdp-${GDP_TYPE} --pop-avg --pop-${POP_TYPE} --sep-close \
	--log --save \
	${REG_TYPE} --reg-${COV_TYPE} --max-lag 11 \
	--ctrl-vars HOST AM YEAR PRE POST GDP POP COMM CLOSE_GMT1 &

python3 -u src/scripts/regression-model/regression_model.py \
	--start-year ${YEAR_START} --gdp-avg --gdp-${GDP_TYPE} --pop-avg --pop-${POP_TYPE} --sep-host --sep-close \
	--log --save \
	${REG_TYPE} --reg-${COV_TYPE} --max-lag 11 \
	--ctrl-vars HOST AM YEAR PRE POST GDP POP COMM CLOSE_GMT1 &


# HOST, CLOSE_WIDE

python3 -u src/scripts/regression-model/regression_model.py \
	--start-year ${YEAR_START} --gdp-avg --gdp-${GDP_TYPE} --pop-avg --pop-${POP_TYPE} \
	--log --save \
	${REG_TYPE} --reg-${COV_TYPE} --max-lag 11 \
	--ctrl-vars HOST AM YEAR PRE POST GDP POP COMM CLOSE_WIDE &

python3 -u src/scripts/regression-model/regression_model.py \
	--start-year ${YEAR_START} --gdp-avg --gdp-${GDP_TYPE} --pop-avg --pop-${POP_TYPE} --sep-host \
	--log --save \
	${REG_TYPE} --reg-${COV_TYPE} --max-lag 11 \
	--ctrl-vars HOST AM YEAR PRE POST GDP POP COMM CLOSE_WIDE &

python3 -u src/scripts/regression-model/regression_model.py \
	--start-year ${YEAR_START} --gdp-avg --gdp-${GDP_TYPE} --pop-avg --pop-${POP_TYPE} --sep-close \
	--log --save \
	${REG_TYPE} --reg-${COV_TYPE} --max-lag 11 \
	--ctrl-vars HOST AM YEAR PRE POST GDP POP COMM CLOSE_WIDE &

python3 -u src/scripts/regression-model/regression_model.py \
	--start-year ${YEAR_START} --gdp-avg --gdp-${GDP_TYPE} --pop-avg --pop-${POP_TYPE} --sep-host --sep-close \
	--log --save \
	${REG_TYPE} --reg-${COV_TYPE} --max-lag 11 \
	--ctrl-vars HOST AM YEAR PRE POST GDP POP COMM CLOSE_WIDE &



wait
