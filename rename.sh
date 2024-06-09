#!/bin/bash

# Directory containing the files
DIR="/Users/diegosiqueira/Playground/numbers/tests"

# Loop through files in the directory
for FILE in "$DIR"/dcode-????; do
  # Check if the file exists and is not a directory
  if [ -f "$FILE" ]; then
    # Extract the 4-digit number from the filename
    BASENAME=$(basename "$FILE")
    NUMBER=${BASENAME:6:4}

    # Construct the new filename
    NEW_FILENAME="$DIR/$NUMBER.png"

    # Rename the file
    mv "$FILE" "$NEW_FILENAME"
  fi
done
