#!/bin/bash

# Define the directory containing the test images and the script to be tested
TEST_DIR="/Users/diegosiqueira/Playground/numbers/tests"
SCRIPT="main4.py"

# Initialize an array to store the results
declare -a RESULTS

# Loop through all PNG files in the test directory
for IMAGE in "$TEST_DIR"/*.png;
do
    # Extract the expected number from the image filename
    FILENAME=$(basename "$IMAGE")
    EXPECTED_NUMBER=${FILENAME%%.*}

    # Run the script with the current image
    OUTPUT=$(python "$SCRIPT" "$IMAGE" 2>&1)

    # Extract the actual number from the output
    ACTUAL_NUMBER=$(echo "$OUTPUT" | awk '/Total sum:/ {print $3}')

    # Check if the script executed successfully and if the numbers match
    if [[ $? -eq 0 && "$ACTUAL_NUMBER" == "$EXPECTED_NUMBER" ]]; then
        RESULTS+=("SUCCESS: $IMAGE - Expected: $EXPECTED_NUMBER, Got: $ACTUAL_NUMBER")
    else
        RESULTS+=("FAILURE: $IMAGE - Expected: $EXPECTED_NUMBER, Got: $ACTUAL_NUMBER, Output: $OUTPUT")
    fi
done

# Print the summary of results
echo "Summary of Test Results:"
for RESULT in "${RESULTS[@]}";
do
    echo "$RESULT"
done
