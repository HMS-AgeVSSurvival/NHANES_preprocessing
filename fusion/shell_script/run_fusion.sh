#!/bin/bash

[ -d out/fusion/ ] || mkdir -p out/fusion/
[ -d error/fusion/ ] || mkdir -p error/fusion/

for MAIN_CATEGORY in "examination" "laboratory" "questionnaire" "demographics" "mortality"
do
    echo -n > out/fusion/$MAIN_CATEGORY.out
    echo -n > error/fusion/$MAIN_CATEGORY.out

    sbatch -J fusion/$MAIN_CATEGORY -o out/fusion/$MAIN_CATEGORY.out -e error/fusion/$MAIN_CATEGORY.out fusion/shell_script/unit_fusion.sh -mc $MAIN_CATEGORY
done