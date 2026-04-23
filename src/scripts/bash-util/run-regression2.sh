#!/bin/bash

# Ensure season parameter is provided and valid
if [[ "$1" != "S" && "$1" != "W" ]]; then
    echo "Usage: $0 <S|W>"
    echo "       S for Summer Olympics"
    echo "       W for Winter Olympics"
    exit 1
fi

SEASON=$1

# ================================
# 1. RUN REGRESSIONS
# ================================

echo "Starting regressions..."

TIMESTAMP=$(date +"%Y%m%d-%H%M%S")
TIMESTAMP_DIR="out/scripts/regression/${TIMESTAMP}"

# Create the exact requested directory structure
mkdir -p "$TIMESTAMP_DIR"


COMMON_ARGS="-s $SEASON --gdp-avg --gdp-log --pop-avg --pop-log --log --save --reg-zinb"

# Function to run a regression instance
run_test() {
	local start_year=$1
	local cov_type=$2
	local with_gpc=$3
	local sep_host_flag=$4
	local sep_close_flag=$5
	local base_vars=$6
	local use_var_boycott=$7
	local use_var_comm=$8
	local min_lag=$9
	local max_lag=${10}

	local args="--start-year $start_year $cov_type"
	local vars="$base_vars"

	if [ "$sep_host_flag" = "true" ];  then args="$args --sep-host";  fi
	if [ "$sep_close_flag" = "true" ]; then args="$args --sep-close"; fi

	# Apply GDP, POP, COMM and adjust lag
	if [ "$with_gpc" = "true" ]; then
		vars="$vars GDP POP"
		if [ "$use_var_comm" = "true" ]; then
			vars="$vars COMM"
		fi
	fi

	# Add Boycott for 1964 if YEAR is NOT in the variables
    if [ "$use_var_boycott" = "true" ] && [ "$start_year" -le 1984 ]; then
        if [[ ! "$base_vars" =~ "YEAR" ]]; then
            vars="$vars BOYCOTT"
        fi
	fi

	args="$args --min-lag $min_lag --max-lag $max_lag"

	python3 -u src/scripts/regression-model/regression_model.py \
		$COMMON_ARGS $args --ctrl-vars $vars &
		
	sleep 0.1 # slight delay to prevent filename timestamp collisions
}



CLOSE_VARS="CLOSE_CENTER CLOSE_GMT1 CLOSE_MAIN CLOSE_WEST CLOSE_WIDE"

for YEAR in 1964 1996; do
	
	if [ "$YEAR" -eq 1996 ]; then COV_TYPE="--reg-hc3"; else COV_TYPE="--reg-hc0"; fi
	

	for WITH_GPC in false true; do

		MIN_LAG=0
		if [ "$WITH_GPC" = "true" ]; then MAX_LAG=11; else MAX_LAG=0; fi
		
		run_test "$YEAR" "$COV_TYPE" "$WITH_GPC" "false" "false" "HOST PRE POST" "true" "true" $MIN_LAG $MAX_LAG

		# YEAR
		run_test "$YEAR" "$COV_TYPE" "$WITH_GPC" "false" "false" "HOST YEAR" "true" "true" $MIN_LAG $MAX_LAG
		run_test "$YEAR" "$COV_TYPE" "$WITH_GPC" "true"  "false" "HOST YEAR" "true" "true" $MIN_LAG $MAX_LAG
		run_test "$YEAR" "$COV_TYPE" "$WITH_GPC" "false" "false" "HOST PRE POST YEAR" "true" "true" $MIN_LAG $MAX_LAG
		run_test "$YEAR" "$COV_TYPE" "$WITH_GPC" "true"  "false" "HOST PRE POST YEAR" "true" "true" $MIN_LAG $MAX_LAG

		# AM
		run_test "$YEAR" "$COV_TYPE" "$WITH_GPC" "true"  "false" "AM HOST"			"true" "true" $MIN_LAG $MAX_LAG
		run_test "$YEAR" "$COV_TYPE" "$WITH_GPC" "false" "false" "AM HOST PRE POST" "true" "true" $MIN_LAG $MAX_LAG

		run_test "$YEAR" "$COV_TYPE" "$WITH_GPC" "false" "true" "AM HOST PRE POST $CLOSE_VARS"	"true" "true" $MIN_LAG $MAX_LAG

		# AM YEAR
		run_test "$YEAR" "$COV_TYPE" "$WITH_GPC" "false" "false" "AM HOST YEAR" "true" "true" $MIN_LAG $MAX_LAG

		wait

	done

	WITH_GPC="true"
	
	# CLOSE
	run_test "$YEAR" "$COV_TYPE" "$WITH_GPC" "true"  "true"  "HOST $CLOSE_VARS" 				"true" "true" $MIN_LAG $MAX_LAG
	run_test "$YEAR" "$COV_TYPE" "$WITH_GPC" "false" "false" "HOST PRE POST $CLOSE_VARS"		"true" "true" $MIN_LAG $MAX_LAG
	run_test "$YEAR" "$COV_TYPE" "$WITH_GPC" "false" "true"  "HOST PRE POST $CLOSE_VARS"		"true" "true" $MIN_LAG $MAX_LAG
	run_test "$YEAR" "$COV_TYPE" "$WITH_GPC" "true"  "true"  "HOST PRE POST $CLOSE_VARS"		"true" "true" $MIN_LAG $MAX_LAG
	run_test "$YEAR" "$COV_TYPE" "$WITH_GPC" "false" "true"  "HOST PRE POST YEAR $CLOSE_VARS"	"true" "true" $MIN_LAG $MAX_LAG
	run_test "$YEAR" "$COV_TYPE" "$WITH_GPC" "false" "true"  "AM HOST PRE POST $CLOSE_VARS"		"true" "true" $MIN_LAG $MAX_LAG

	# lags 12 to 28, with a step of 4
	for MIN_LAG in 12 16 20 24 28; do

		MAX_LAG=$MIN_LAG

		run_test "$YEAR" "$COV_TYPE" "$WITH_GPC" "true"  "false" "HOST PRE POST"		"true" "true" $MIN_LAG $MAX_LAG
		run_test "$YEAR" "$COV_TYPE" "$WITH_GPC" "false" "false" "AM HOST PRE POST"		"true" "true" $MIN_LAG $MAX_LAG
		run_test "$YEAR" "$COV_TYPE" "$WITH_GPC" "true"  "false" "AM HOST PRE POST"		"true" "true" $MIN_LAG $MAX_LAG
		run_test "$YEAR" "$COV_TYPE" "$WITH_GPC" "true"  "false" "HOST PRE POST YEAR"	"true" "true" $MIN_LAG $MAX_LAG

		wait
	done


	COV_TYPE=""
	MIN_LAG=0
	MAX_LAG=11

	run_test "$YEAR" "$COV_TYPE" "$WITH_GPC" "false" "false" "HOST PRE POST YEAR $CLOSE_VARS"	"true" "true" $MIN_LAG $MAX_LAG
	run_test "$YEAR" "$COV_TYPE" "$WITH_GPC" "false" "true"  "HOST PRE POST $CLOSE_VARS"		"true" "true" $MIN_LAG $MAX_LAG
	run_test "$YEAR" "$COV_TYPE" "$WITH_GPC" "true"  "true"  "HOST $CLOSE_VARS"					"true" "true" $MIN_LAG $MAX_LAG


done



YEAR=1964
COV_TYPE="--reg-hc0"

WITH_GPC="true"
MIN_LAG=0
MAX_LAG=11
		
run_test "$YEAR" "$COV_TYPE" "$WITH_GPC" "true" "false" "HOST PRE POST"			"false" "true" $MIN_LAG $MAX_LAG
run_test "$YEAR" "$COV_TYPE" "$WITH_GPC" "true" "false" "HOST PRE POST"			"true"  "true" $MIN_LAG $MAX_LAG
run_test "$YEAR" "$COV_TYPE" "$WITH_GPC" "true" "false" "AM HOST PRE POST"		"false" "true" $MIN_LAG $MAX_LAG
run_test "$YEAR" "$COV_TYPE" "$WITH_GPC" "true" "false" "AM HOST PRE POST"		"true"  "true" $MIN_LAG $MAX_LAG
run_test "$YEAR" "$COV_TYPE" "$WITH_GPC" "true" "false" "HOST PRE POST YEAR"	"false" "true" $MIN_LAG $MAX_LAG
run_test "$YEAR" "$COV_TYPE" "$WITH_GPC" "true" "false" "HOST PRE POST YEAR"	"true"  "true" $MIN_LAG $MAX_LAG

run_test "$YEAR" "$COV_TYPE" "$WITH_GPC" "true" "false" "HOST PRE POST"			"true" "false" $MIN_LAG $MAX_LAG
run_test "$YEAR" "$COV_TYPE" "$WITH_GPC" "true" "false" "HOST PRE POST YEAR"	"true" "false" $MIN_LAG $MAX_LAG
run_test "$YEAR" "$COV_TYPE" "$WITH_GPC" "true" "false" "AM HOST PRE POST"		"true" "false" $MIN_LAG $MAX_LAG

wait



YEAR=1996
COV_TYPE="--reg-hc3"

for WITH_GPC in false true; do

	MIN_LAG=0
	if [ "$WITH_GPC" = "true" ]; then MAX_LAG=11; else MAX_LAG=0; fi

	run_test "$YEAR" "$COV_TYPE" "$WITH_GPC" "true" "false" "HOST PRE POST"			"true" "true" $MIN_LAG $MAX_LAG
	run_test "$YEAR" "$COV_TYPE" "$WITH_GPC" "true" "false" "HOST PRE POST YEAR"	"true" "true" $MIN_LAG $MAX_LAG
	# CLOSE
	run_test "$YEAR" "$COV_TYPE" "$WITH_GPC" "true" "false" "HOST PRE POST YEAR $CLOSE_VARS" "true" "true" $MIN_LAG $MAX_LAG

done

WITH_GPC="true"
MIN_LAG=0
MAX_LAG=11

run_test "$YEAR" "$COV_TYPE" "$WITH_GPC" "true" "false" "HOST PRE POST YEAR CLOSE_WIDE" "true" "true" $MIN_LAG $MAX_LAG
run_test "$YEAR" "$COV_TYPE" "$WITH_GPC" "true" "false" "HOST PRE POST YEAR COMM"		"true" "true" $MIN_LAG $MAX_LAG
run_test "$YEAR" "$COV_TYPE" "$WITH_GPC" "true" "false" "AM HOST PRE POST"				"true" "true" $MIN_LAG $MAX_LAG
run_test "$YEAR" "$COV_TYPE" "$WITH_GPC" "true" "false" "AM HOST PRE POST COMM" 		"true" "true" $MIN_LAG $MAX_LAG

wait



COV_TYPE="--reg-hc0"

for YEAR in 1932 1896; do

	run_test "$YEAR" "$COV_TYPE" "$WITH_GPC" "true"  "false" "HOST PRE POST"		"true" "true" $MIN_LAG $MAX_LAG
	run_test "$YEAR" "$COV_TYPE" "$WITH_GPC" "false" "false" "AM HOST PRE POST"		"true" "true" $MIN_LAG $MAX_LAG
	run_test "$YEAR" "$COV_TYPE" "$WITH_GPC" "true"  "false" "AM HOST PRE POST"		"true" "true" $MIN_LAG $MAX_LAG
	run_test "$YEAR" "$COV_TYPE" "$WITH_GPC" "true"  "false" "HOST PRE POST YEAR"	"true" "true" $MIN_LAG $MAX_LAG

	# CLOSE
	run_test "$YEAR" "$COV_TYPE" "$WITH_GPC" "true"  "true"  "HOST $CLOSE_VARS"				"true" "true" $MIN_LAG $MAX_LAG
	run_test "$YEAR" "$COV_TYPE" "$WITH_GPC" "false" "false" "HOST PRE POST $CLOSE_VARS"	"true" "true" $MIN_LAG $MAX_LAG
	run_test "$YEAR" "$COV_TYPE" "$WITH_GPC" "false" "true"  "AM HOST PRE POST $CLOSE_VARS"	"true" "true" $MIN_LAG $MAX_LAG

done



echo "Waiting for all background processes to finish..."
wait
echo "Regressions complete."

# ================================
# 2. AUTOMATED FILE SORTING
# ================================

echo "Sorting log files into directory structure..."

BASE_OUT="out/scripts/regression"

# Find all files in the current run (maxdepth 1)
# Naming pattern: *sep-closeX_VAR1+VAR2*
find "$BASE_OUT" -maxdepth 1 -type f -name "*sep-close*" -print0 | while IFS= read -r -d '' FILE; do
    FILENAME=$(basename "$FILE")

    # 1. Extract the variable part after sep-closeX_
    # Matches everything between 'sep-close' + one digit + '_' and the next '.' or end of string
	VARS_PART=$(echo "$FILENAME" | sed -E 's/.*sep-close[0-9]_(.*)_\..*/\1/')

    # 2. Extract flags
    SEP_HOST=$(echo "$FILENAME" | grep -o "sep-host[0-1]" | sed 's/sep-host//')
    SEP_CLOSE=$(echo "$FILENAME" | grep -o "sep-close[0-1]" | sed 's/sep-close//')

    # 3. Clean VARS_PART: Remove G, B, P, C if they are isolated (not part of a word)
    # This handles GDP, POP, COMM, BOYCOTT by only matching single letters G, B, P, C 
    # surrounded by '+' or at boundaries.
    CLEAN_VARS=$(echo "$VARS_PART" | sed -E 's/\b(G|B|P|C)\b//g' | sed -E 's/\+\+/\+/g' | sed 's/^\+//;s/\+$//')
    
    # 4. Construct folder name
    # Replace '+' with '-' and handle abbreviations if preferred (e.g., 'Pr+Po' -> 'Pre-Post')
    DIR_NAME=$(echo "$CLEAN_VARS" | sed 's/\+/ /g' | xargs | sed 's/ /-/g')

    # Handle the "AM HOST" vs "HOST" prefixing logic if needed, 
    # but based on your request, we use the extracted part.
    if [ -z "$DIR_NAME" ]; then DIR_NAME="Baseline"; fi

    # 5. Append suffix based on flags
    SUFFIX=""
    if [ "$SEP_HOST" -eq 1 ] && [ "$SEP_CLOSE" -eq 1 ]; then
        SUFFIX="_sep-host-close"
    elif [ "$SEP_HOST" -eq 1 ]; then
        SUFFIX="_sep-host"
    elif [ "$SEP_CLOSE" -eq 1 ]; then
        SUFFIX="_sep-close"
    fi
    
    FINAL_DIR="$TIMESTAMP_DIR/${DIR_NAME}${SUFFIX}"

    # 6. Move the file
    mkdir -p "$FINAL_DIR"
    mv "$FILE" "$FINAL_DIR/"
done

echo "All logs processed and moved to $TIMESTAMP_DIR successfully."