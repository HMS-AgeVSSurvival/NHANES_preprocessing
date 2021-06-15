#!/bin/bash

for MAIN_CATEGORY in "examination" "laboratory" "questionnaire"
do
    for PATH_CATEGORY in casting/data/$MAIN_CATEGORY/*
    do
        IFS='/' read -r a a a FILE_CATEGORY <<<"$PATH_CATEGORY"
        CATEGORY=$(echo $FILE_CATEGORY | cut -d "." -f 1)

        rm out/merge/$MAIN_CATEGORY/$CATEGORY.out
        sbatch -J merge/$MAIN_CATEGORY/$CATEGORY -o out/merge/$MAIN_CATEGORY/$CATEGORY.out merge/shell_script/unit_merge.sh -mc $MAIN_CATEGORY -c $CATEGORY
    done
done