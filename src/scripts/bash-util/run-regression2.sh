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

	local args="--start-year $start_year $cov_type"
	local vars="$base_vars"
	local lag=1

	if [ "$sep_host_flag" = "true" ];  then args="$args --sep-host";  fi
	if [ "$sep_close_flag" = "true" ]; then args="$args --sep-close"; fi

	# Apply GDP, POP, COMM and adjust lag
	if [ "$with_gpc" = "true" ]; then
		vars="$vars GDP POP COMM"
		#lag=11
		lag=1
	fi

	# Add Boycott for 1964 if YEAR is NOT in the variables
	if [ "$start_year" -eq 1964 ]; then
		if [[ ! "$base_vars" =~ "YEAR" ]]; then
			vars="$vars BOYCOTT"
		fi
	fi

	args="$args --max-lag $lag"

	python3 -u src/scripts/regression-model/regression_model.py \
		$COMMON_ARGS $args --ctrl-vars $vars &
		
	sleep 0.1 # slight delay to prevent filename timestamp collisions
}

for YEAR in 1964 1996; do
	
	
	for WITH_GPC in false true; do

		if [ "$YEAR" -eq 1996 ]; then COV_TYPE="--reg-hc3"; else COV_TYPE="--reg-hc0"; fi
		
		run_test "$YEAR" "$COV_TYPE" "$WITH_GPC" "false" "false" "HOST"
		run_test "$YEAR" "$COV_TYPE" "$WITH_GPC" "false" "false" "HOST PRE POST"
		run_test "$YEAR" "$COV_TYPE" "$WITH_GPC" "true"  "false" "HOST PRE POST"
		
		CLOSE_VARS="HOST PRE POST CLOSE_CENTER CLOSE_GMT1 CLOSE_MAIN CLOSE_WEST CLOSE_WIDE"
		run_test "$YEAR" "$COV_TYPE" "$WITH_GPC" "false" "false" "$CLOSE_VARS"
		run_test "$YEAR" "$COV_TYPE" "$WITH_GPC" "false" "true"  "$CLOSE_VARS"

		CLOSE_VARS="HOST CLOSE_CENTER CLOSE_GMT1 CLOSE_MAIN CLOSE_WEST CLOSE_WIDE"
		run_test "$YEAR" "$COV_TYPE" "$WITH_GPC" "false" "false" "$CLOSE_VARS"
		run_test "$YEAR" "$COV_TYPE" "$WITH_GPC" "false" "true"  "$CLOSE_VARS"
		run_test "$YEAR" "$COV_TYPE" "$WITH_GPC" "true"  "false" "$CLOSE_VARS"
		run_test "$YEAR" "$COV_TYPE" "$WITH_GPC" "true"  "true"  "$CLOSE_VARS"

		CLOSE_VARS="HOST PRE POST CLOSE_WIDE"
		run_test "$YEAR" "$COV_TYPE" "$WITH_GPC" "false" "false" "$CLOSE_VARS"
		run_test "$YEAR" "$COV_TYPE" "$WITH_GPC" "false" "true"  "$CLOSE_VARS"
		run_test "$YEAR" "$COV_TYPE" "$WITH_GPC" "true"  "false" "$CLOSE_VARS"
		run_test "$YEAR" "$COV_TYPE" "$WITH_GPC" "true"  "true"  "$CLOSE_VARS"

		wait

		CLOSE_VARS="HOST PRE POST CLOSE_GMT1"
		run_test "$YEAR" "$COV_TYPE" "$WITH_GPC" "false" "false" "$CLOSE_VARS"
		run_test "$YEAR" "$COV_TYPE" "$WITH_GPC" "false" "true"  "$CLOSE_VARS"
		run_test "$YEAR" "$COV_TYPE" "$WITH_GPC" "true"  "false" "$CLOSE_VARS"
		run_test "$YEAR" "$COV_TYPE" "$WITH_GPC" "true"  "true"  "$CLOSE_VARS"

		CLOSE_VARS="HOST PRE POST CLOSE_CENTER"
		run_test "$YEAR" "$COV_TYPE" "$WITH_GPC" "false" "false" "$CLOSE_VARS"
		run_test "$YEAR" "$COV_TYPE" "$WITH_GPC" "false" "true"  "$CLOSE_VARS"
		run_test "$YEAR" "$COV_TYPE" "$WITH_GPC" "true"  "false" "$CLOSE_VARS"
		run_test "$YEAR" "$COV_TYPE" "$WITH_GPC" "true"  "true"  "$CLOSE_VARS"

		CLOSE_VARS="HOST PRE POST CLOSE_MAIN"
		run_test "$YEAR" "$COV_TYPE" "$WITH_GPC" "false" "false" "$CLOSE_VARS"
		run_test "$YEAR" "$COV_TYPE" "$WITH_GPC" "false" "true"  "$CLOSE_VARS"
		run_test "$YEAR" "$COV_TYPE" "$WITH_GPC" "true"  "false" "$CLOSE_VARS"
		run_test "$YEAR" "$COV_TYPE" "$WITH_GPC" "true"  "true"  "$CLOSE_VARS"

		CLOSE_VARS="HOST PRE POST CLOSE_WEST"
		run_test "$YEAR" "$COV_TYPE" "$WITH_GPC" "false" "false" "$CLOSE_VARS"
		run_test "$YEAR" "$COV_TYPE" "$WITH_GPC" "false" "true"  "$CLOSE_VARS"
		run_test "$YEAR" "$COV_TYPE" "$WITH_GPC" "true"  "false" "$CLOSE_VARS"
		run_test "$YEAR" "$COV_TYPE" "$WITH_GPC" "true"  "true"  "$CLOSE_VARS"

		wait
		

		# YEAR

		run_test "$YEAR" "$COV_TYPE" "$WITH_GPC" "true" "false" "HOST PRE POST YEAR"

		CLOSE_VARS="HOST PRE POST YEAR CLOSE_CENTER CLOSE_GMT1 CLOSE_MAIN CLOSE_WEST CLOSE_WIDE"
		run_test "$YEAR" "$COV_TYPE" "$WITH_GPC" "false" "false" "$CLOSE_VARS"
		run_test "$YEAR" "$COV_TYPE" "$WITH_GPC" "false" "true"  "$CLOSE_VARS"

		CLOSE_VARS="HOST YEAR CLOSE_CENTER CLOSE_GMT1 CLOSE_MAIN CLOSE_WEST CLOSE_WIDE"
		run_test "$YEAR" "$COV_TYPE" "$WITH_GPC" "false" "false" "$CLOSE_VARS"
		run_test "$YEAR" "$COV_TYPE" "$WITH_GPC" "false" "true"  "$CLOSE_VARS"
		run_test "$YEAR" "$COV_TYPE" "$WITH_GPC" "true"  "false" "$CLOSE_VARS"

		CLOSE_VARS="HOST PRE POST YEAR CLOSE_WIDE"
		run_test "$YEAR" "$COV_TYPE" "$WITH_GPC" "true" "false" "$CLOSE_VARS"
		run_test "$YEAR" "$COV_TYPE" "$WITH_GPC" "true" "true"  "$CLOSE_VARS"

		CLOSE_VARS="HOST PRE POST CLOSE_GMT1"
		run_test "$YEAR" "$COV_TYPE" "$WITH_GPC" "true" "false" "$CLOSE_VARS"
		run_test "$YEAR" "$COV_TYPE" "$WITH_GPC" "true" "true"  "$CLOSE_VARS"

		wait


		# AM

		run_test "$YEAR" "$COV_TYPE" "$WITH_GPC" "false" "false" "HOST"
		run_test "$YEAR" "$COV_TYPE" "$WITH_GPC" "false" "false" "HOST PRE POST"
		run_test "$YEAR" "$COV_TYPE" "$WITH_GPC" "true"  "false" "HOST PRE POST"
		
		
		# CLOSE variations (Am-Host-Pre-Post-Close)
		CLOSE_VARS="AM HOST PRE POST CLOSE_CENTER CLOSE_GMT1 CLOSE_MAIN CLOSE_WEST CLOSE_WIDE"
		run_test "$YEAR" "$COV_TYPE" "$WITH_GPC" "false" "false" "$CLOSE_VARS"
		run_test "$YEAR" "$COV_TYPE" "$WITH_GPC" "true"  "true"  "$CLOSE_VARS"

		CLOSE_VARS="AM HOST CLOSE_CENTER CLOSE_GMT1 CLOSE_MAIN CLOSE_WEST CLOSE_WIDE"
		run_test "$YEAR" "$COV_TYPE" "$WITH_GPC" "false" "false" "$CLOSE_VARS"
		run_test "$YEAR" "$COV_TYPE" "$WITH_GPC" "false" "true"  "$CLOSE_VARS"


		# AM YEAR

		run_test "$YEAR" "$COV_TYPE" "$WITH_GPC" "false" "false" "AM HOST YEAR"
		run_test "$YEAR" "$COV_TYPE" "$WITH_GPC" "true"  "false" "AM HOST YEAR"

		wait

	done
done



YEAR=1996
COV_TYPE="--reg-hc3"

for WITH_GPC in false true; do

	run_test "$YEAR" "$COV_TYPE" "$WITH_GPC" "false" "false" "HOST YEAR"
	run_test "$YEAR" "$COV_TYPE" "$WITH_GPC" "false" "false" "HOST PRE POST YEAR"

	CLOSE_VARS="HOST PRE POST YEAR CLOSE_CENTER CLOSE_GMT1 CLOSE_MAIN CLOSE_WEST CLOSE_WIDE"
	run_test "$YEAR" "$COV_TYPE" "$WITH_GPC" "false" "false" "$CLOSE_VARS"
	run_test "$YEAR" "$COV_TYPE" "$WITH_GPC" "false" "true"  "$CLOSE_VARS"
	run_test "$YEAR" "$COV_TYPE" "$WITH_GPC" "true"  "false" "$CLOSE_VARS"
	run_test "$YEAR" "$COV_TYPE" "$WITH_GPC" "true"  "true"  "$CLOSE_VARS"
	
	wait

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