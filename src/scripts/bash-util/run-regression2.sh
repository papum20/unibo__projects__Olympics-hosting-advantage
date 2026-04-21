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
mkdir -p "$TIMESTAMP_DIR/Am-Host/"
mkdir -p "$TIMESTAMP_DIR/Am-Host-Year/"

mkdir -p "$TIMESTAMP_DIR/Am-Host-Pre-Post/"
mkdir -p "$TIMESTAMP_DIR/Am-Host-Pre-Post_sep-host/"

mkdir -p "$TIMESTAMP_DIR/Am-Host-Pre-Post-Close/"
mkdir -p "$TIMESTAMP_DIR/Am-Host-Pre-Post-Close_sep-close/"

mkdir -p "$TIMESTAMP_DIR/Am-Host-Close/"
mkdir -p "$TIMESTAMP_DIR/Am-Host-Close_sep-close/"
mkdir -p "$TIMESTAMP_DIR/Am-Host-Close_sep-host/"
mkdir -p "$TIMESTAMP_DIR/Am-Host-Close_sep-host-close/"

mkdir -p "$TIMESTAMP_DIR/Am-Host-Pre-Post-Close-gmt1_sep-host/"
mkdir -p "$TIMESTAMP_DIR/Am-Host-Pre-Post-Close-gmt1_sep-host-close/"
mkdir -p "$TIMESTAMP_DIR/Am-Host-Pre-Post-Close-wide_sep-host/"
mkdir -p "$TIMESTAMP_DIR/Am-Host-Pre-Post-Close-wide_sep-host-close/"

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

	if [ "$sep_host_flag" = "true" ]; then args="$args --sep-host"; fi
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
		
		#ok with AM
		run_test "$YEAR" "$COV_TYPE" "$WITH_GPC" "false" "false" "HOST"
		#ok with AM
		run_test "$YEAR" "$COV_TYPE" "$WITH_GPC" "false" "false" "HOST YEAR"
		#ok with AM
		run_test "$YEAR" "$COV_TYPE" "$WITH_GPC" "false" "false" "HOST PRE POST"
		
		
		# CLOSE variations (Am-Host-Pre-Post-Close)
		CLOSE_VARS="HOST PRE POST CLOSE_CENTER CLOSE_GMT1 CLOSE_MAIN CLOSE_WEST CLOSE_WIDE"
		
		#ok with AM
		run_test "$YEAR" "$COV_TYPE" "$WITH_GPC" "false" "false" "$CLOSE_VARS" # standard
		#ok with AM
		run_test "$YEAR" "$COV_TYPE" "$WITH_GPC" "false" "true" "$CLOSE_VARS"  # sep-close

		CLOSE_VARS="HOST CLOSE_CENTER CLOSE_GMT1 CLOSE_MAIN CLOSE_WEST CLOSE_WIDE"
		
		#ok with AM
		run_test "$YEAR" "$COV_TYPE" "$WITH_GPC" "false" "false" "$CLOSE_VARS" # standard
		#ok with AM
		run_test "$YEAR" "$COV_TYPE" "$WITH_GPC" "false" "true" "$CLOSE_VARS"  # sep-close

		run_test "$YEAR" "$COV_TYPE" "$WITH_GPC" "true" "false" "$CLOSE_VARS"  # sep-host
		run_test "$YEAR" "$COV_TYPE" "$WITH_GPC" "true" "true" "$CLOSE_VARS"   # sep-host-close

		CLOSE_VARS="HOST PRE POST CLOSE_WIDE"

		run_test "$YEAR" "$COV_TYPE" "$WITH_GPC" "true" "false" "$CLOSE_VARS"  # sep-host
		run_test "$YEAR" "$COV_TYPE" "$WITH_GPC" "true" "true" "$CLOSE_VARS"   # sep-host-close

		CLOSE_VARS="HOST PRE POST CLOSE_GMT1"

		run_test "$YEAR" "$COV_TYPE" "$WITH_GPC" "true" "false" "$CLOSE_VARS"  # sep-host
		run_test "$YEAR" "$COV_TYPE" "$WITH_GPC" "true" "true" "$CLOSE_VARS"   # sep-host-close

		# Am-Host-Pre-Post_sep-host
		#ok with AM
		run_test "$YEAR" "$COV_TYPE" "$WITH_GPC" "true" "false" "HOST PRE POST"

	done
done

echo "Waiting for all background processes to finish..."
wait
echo "Regressions complete."

# ================================
# 2. FILE SORTING
# ================================

echo "Sorting log files into directory structure..."

BASE_OUT="out/scripts/regression"

# 1. Move CLOSE variants first (most specific)
find "$BASE_OUT" -maxdepth 1 -type f -name '*sep-host0*' -name '*sep-close1*' -name '*Pr+Po*' -name '*CC+CG1+CM+CW+Cwd*' -exec mv {} "$TIMESTAMP_DIR/Am-Host-Pre-Post-Close_sep-close/" \;
find "$BASE_OUT" -maxdepth 1 -type f -name '*sep-host0*' -name '*sep-close0*' -name '*Pr+Po*' -name '*CC+CG1+CM+CW+Cwd*' -exec mv {} "$TIMESTAMP_DIR/Am-Host-Pre-Post-Close/" \;

find "$BASE_OUT" -maxdepth 1 -type f -name '*sep-host0*' -name '*sep-close0*' -name '*CC+CG1+CM+CW+Cwd*' -exec mv {} "$TIMESTAMP_DIR/Am-Host-Close/" \;
find "$BASE_OUT" -maxdepth 1 -type f -name '*sep-host0*' -name '*sep-close1*' -name '*CC+CG1+CM+CW+Cwd*' -exec mv {} "$TIMESTAMP_DIR/Am-Host-Close_sep-close/" \;
find "$BASE_OUT" -maxdepth 1 -type f -name '*sep-host1*' -name '*sep-close0*' -name '*CC+CG1+CM+CW+Cwd*' -exec mv {} "$TIMESTAMP_DIR/Am-Host-Close_sep-host/" \;
find "$BASE_OUT" -maxdepth 1 -type f -name '*sep-host1*' -name '*sep-close1*' -name '*CC+CG1+CM+CW+Cwd*' -exec mv {} "$TIMESTAMP_DIR/Am-Host-Close_sep-host-close/" \;

find "$BASE_OUT" -maxdepth 1 -type f -name '*sep-host1*' -name '*sep-close1*' -name '*CG1*' -exec mv {} "$TIMESTAMP_DIR/Am-Host-Pre-Post-Close-gmt1_sep-host-close/" \;
find "$BASE_OUT" -maxdepth 1 -type f -name '*sep-host1*' -name '*sep-close0*' -name '*CG1*' -exec mv {} "$TIMESTAMP_DIR/Am-Host-Pre-Post-Close-gmt1_sep-host/" \;
find "$BASE_OUT" -maxdepth 1 -type f -name '*sep-host1*' -name '*sep-close1*' -name '*Cwd*' -exec mv {} "$TIMESTAMP_DIR/Am-Host-Pre-Post-Close-wide_sep-host-close/" \;
find "$BASE_OUT" -maxdepth 1 -type f -name '*sep-host1*' -name '*sep-close0*' -name '*Cwd*' -exec mv {} "$TIMESTAMP_DIR/Am-Host-Pre-Post-Close-wide_sep-host/" \;

# 2. Move PRE+POST variants (excluding CLOSE which are already moved)
find "$BASE_OUT" -maxdepth 1 -type f -name "*+Pr+Po*" -name "*sep-host1*" -exec mv {} "$TIMESTAMP_DIR/Am-Host-Pre-Post_sep-host/" \;
find "$BASE_OUT" -maxdepth 1 -type f -name "*+Pr+Po*" -name "*sep-host0*" -exec mv {} "$TIMESTAMP_DIR/Am-Host-Pre-Post/" \;

# 3. Move YEAR variants (excluding PRE+POST and CLOSE which are already moved)
find "$BASE_OUT" -maxdepth 1 -type f -name "*+Y*" -name "*sep-host0*" -exec mv {} "$TIMESTAMP_DIR/Am-Host-Year/" \;

# 4. Move baseline AM+HOST variants (Everything else remaining)
find "$BASE_OUT" -maxdepth 1 -type f -name "*M+H*" -name "*sep-host0*" -exec mv {} "$TIMESTAMP_DIR/Am-Host/" \;

echo "All logs processed and moved to $TIMESTAMP_DIR successfully."