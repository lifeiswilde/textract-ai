#!/bin/bash

IMAGE_FOLDER="./output/images_output"

# Find and sort files by their numerical order, then process each with Tesseract
find "$IMAGE_FOLDER" -type f \( -iname "*.jpg" -o -iname "*.png" \) | sort -V | while read image_file; do
    echo "Processing $image_file with Tesseract-OCR..."
    tesseract "$image_file" stdout
    echo "-----------------------------------------------------"
done

