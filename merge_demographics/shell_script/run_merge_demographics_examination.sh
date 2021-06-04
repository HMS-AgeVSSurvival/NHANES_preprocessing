#!/bin/bash

for CATEGORY in "body" "eyes" "ears" "nose_mouth" "lungs" "heart" "liver" "bones" "nerves" "muscles" "skin" "physical_activity" "other"
do
    rm out/merge_demographics/examination/$CATEGORY.out
    sbatch -J merge_demographics/examination/$CATEGORY -o out/merge_demographics/examination/$CATEGORY.out merge_demographics/shell_script/unit_merge_demographics.sh -mc "examination" -c $CATEGORY
done