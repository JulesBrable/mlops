#!/bin/bash

URL="https://data.opendatasoft.com/api/explore/v2.1/catalog/datasets/que-faire-a-paris-@parisdata/exports/json?lang=fr"
BUCKET_NAME="jbrablx"
TODAY=$(date +%Y%m%d-%H)
FILENAME="test_${TODAY}.csv"
TARGET_PATH="mlops/data/raw/${FILENAME}"
TEMP_FILE="/tmp/${FILENAME}"

python3 fetch_data.py $URL $TEMP_FILE

if [ -s $TEMP_FILE ]; then
    echo "CSV file created successfully."

    mc cp $TEMP_FILE s3/${BUCKET_NAME}/${TARGET_PATH}
    if [ $? -eq 0 ]; then
        echo "File uploaded successfully to MinIO."

        mc anonymous set download s3/${BUCKET_NAME}/${TARGET_PATH}
        if [ $? -eq 0 ]; then
            echo "File permissions set to downloadable."
        else
            echo "Failed to set file permissions."
        fi
    else
        echo "Failed to upload file to MinIO."
    fi
else
    echo "Failed to create CSV file or file is empty."
fi
