#!/bin/bash

for CATEGORY in "body" "eyes" "ears" "nose_mouth" "lungs" "heart" "liver" "bones" "nerves" "muscles" "skin" "physical_activity" "other"
do
    rm out/cleaning/examination/$CATEGORY.out
    sbatch -J cleaning/examination/$CATEGORY -o out/cleaning/examination/$CATEGORY.out cleaning/shell_script/unit_cleaning_examination.sh -c $CATEGORY -n 20
done