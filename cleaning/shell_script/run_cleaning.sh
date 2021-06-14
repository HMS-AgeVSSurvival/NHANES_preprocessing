#!/bin/bash

for MAIN_CATEGORY in "examination" "laboratory" "questionnaire" "demographics" "mortality"
do
    for PATH_CATEGORY in fusion/data/$MAIN_CATEGORY/*
    do
        IFS='/' read -r a a a FILE_CATEGORY <<<"$PATH_CATEGORY"
        CATEGORY=$(echo $FILE_CATEGORY | cut -d "." -f 1)

        rm out/cleaning/$MAIN_CATEGORY/$CATEGORY.out
        sbatch -J cleaning/$MAIN_CATEGORY/$CATEGORY -o out/cleaning/$MAIN_CATEGORY/$CATEGORY.out cleaning/shell_script/unit_cleaning.sh -mc $MAIN_CATEGORY -c $CATEGORY -n 20
    done
done