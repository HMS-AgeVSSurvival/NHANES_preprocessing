#!/bin/bash

for MAIN_CATEGORY in "examination" "laboratory" "questionnaire" "demographics" "mortality"
do
    rm out/correlation_with_age/$MAIN_CATEGORY.out
    sbatch -J correlation_with_age/$MAIN_CATEGORY -o out/correlation_with_age/$MAIN_CATEGORY.out correlation_with_age/shell_script/unit_correlation_with_age.sh -mc $MAIN_CATEGORY
done