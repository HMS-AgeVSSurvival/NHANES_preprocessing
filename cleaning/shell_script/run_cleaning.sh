#!/bin/bash

for MAIN_CATEGORY in "examination" "laboratory" "questionnaire" "demographics" "mortality"
do
    [ -d out/cleaning/$MAIN_CATEGORY ] || mkdir -p out/cleaning/$MAIN_CATEGORY
    [ -d error/cleaning/$MAIN_CATEGORY ] || mkdir -p error/cleaning/$MAIN_CATEGORY
    
    for PATH_CATEGORY in fusion/data/$MAIN_CATEGORY/*
    do
        IFS='/' read -r a a a FILE_CATEGORY <<<"$PATH_CATEGORY"
        CATEGORY=$(echo $FILE_CATEGORY | cut -d "." -f 1)

        echo -n > out/cleaning/$MAIN_CATEGORY/$CATEGORY.out
        echo -n > error/cleaning/$MAIN_CATEGORY/$CATEGORY.out

        sbatch -J cleaning/$MAIN_CATEGORY/$CATEGORY -o out/cleaning/$MAIN_CATEGORY/$CATEGORY.out -e error/cleaning/$MAIN_CATEGORY/$CATEGORY.out cleaning/shell_script/unit_cleaning.sh -mc $MAIN_CATEGORY -c $CATEGORY -n 20
    done
done