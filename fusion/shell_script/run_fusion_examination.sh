#!/bin/bash

for CATEGORY in "body" "eyes" "ears" "nose_mouth" "lungs" "heart" "liver" "bones" "nerves" "muscles" "skin" "physical_activity" "other"
do
    rm out/fusion/examination/$CATEGORY.out
    sbatch -J fusion/examination/$CATEGORY -o out/fusion/examination/$CATEGORY.out fusion/shell_script/unit_fusion.sh -mc "examination" -c $CATEGORY
done