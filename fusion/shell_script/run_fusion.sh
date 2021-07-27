#!/bin/bash

for MAIN_CATEGORY in "examination" "laboratory" "questionnaire" "demographics" "mortality"
do
    rm out/fusion/$MAIN_CATEGORY.out
    sbatch -J fusion/$MAIN_CATEGORY -o out/fusion/$MAIN_CATEGORY.out fusion/shell_script/unit_fusion.sh -mc $MAIN_CATEGORY
done