#!/bin/bash

# t1blgm_analysis.sh
# Description: Script for T1 BLGM analysis

# Usage: ./t1blgm_analysis.sh <folder_path>
# the <folder_path> is the folder containing the T1 BLGM data that need to be placed to MNI space

FOLDER_PATH=$1

if [ -z "$FOLDER_PATH" ]; then
    echo "Usage: $0 <folder_path>"
    exit 1
fi

# Check if the folder exists
if [ ! -d "$FOLDER_PATH" ]; then
    echo "Error: Folder '$FOLDER_PATH' does not exist."
    exit 1
fi  

if [[ "$(basename "$FOLDER_PATH")" == "CTR" ]]; then
    group_type="control"
elif [[ "$(basename "$FOLDER_PATH")" == "DFC" ]]; then
    group_type="patient"
else
    echo "Error: Folder name must be either 'CTR' or 'DFC'."
    exit 1
fi


counter=1
for folder in $(ls $FOLDER_PATH); do
    if [ -d "$folder" ]; then
        echo "Processing folder: $folder"
        # Check if the folder contains the required files
        if [ ! -f "$folder/t1blgm_corr.nii.gz" ]; then
            echo "Error: t1blgm_corr.nii.gz not found in $folder"
            exit 1
        fi
    fi

    full_path="$FOLDER_PATH/$folder"

    # Make the flipped image for the T1 blgm
    echo "Creating flipped image for T1 BLGM..."
    fslswapdim $full_path/t1blgm_corr.nii.gz x -y z $full_path/t1blgm_corr_flipped.nii.gz

    # Adjust the image header information
    echo "Adjusting image header information..."
    m0_fliped="$full_path/m0_fliped.nii.gz"
    t1blgm_corr_flipped="$full_path/t1blgm_corr_flipped.nii.gz"
    t1blgm_corr_flipped_header="$full_path/t1blgm_corr_flipped_header.nii.gz"
    CopyImageHeaderInformation $m0_fliped $t1blgm_corr_flipped $t1blgm_corr_flipped_header 1 1 1

    # Apply the transformation to MNI space
    echo "Applying transformation to MNI space..."
    antsApplyTransforms -d 3 -i $t1blgm_corr_flipped_header -r ~/fsl/data/standard/MNI152_T1_2mm.nii.gz -o $full_path/${group_type}_t1blgm_mni_${counter}.nii.gz -t $full_path/mni_1Warp.nii.gz -t $full_path/mni_0GenericAffine.mat

    echo "-----------------------------------------"
    echo "Transformation applied for folder: $folder"
    echo "Output saved as: $full_path/${group_type}_t1blgm_mni_${counter}.nii.gz"
    echo "-----------------------------------------"
    ((counter++))
done