#!/bin/bash

for CATEGORY in "body" "eyes" "ears" "nose_mouth" "lungs" "heart" "liver" "bones" "nerves" "muscles" "skin" "physical_activity" "other"
do
    rm out/casting/examination/$CATEGORY.out
    sbatch -J casting/examination/$CATEGORY -o out/casting/examination/$CATEGORY.out casting/shell_script/unit_casting_examination.sh -c $CATEGORY
done