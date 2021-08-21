#!/bin/bash

for MAIN_CATEGORY in "examination" "laboratory" "questionnaire"
do
    [ -d out/merge/$MAIN_CATEGORY/ ] || mkdir -p out/merge/$MAIN_CATEGORY/
    [ -d error/merge/$MAIN_CATEGORY/ ] || mkdir -p error/merge/$MAIN_CATEGORY/

    for PATH_CATEGORY in casting/data/$MAIN_CATEGORY/*
    do
        IFS='/' read -r a a a FILE_CATEGORY <<<"$PATH_CATEGORY"
        CATEGORY=$(echo $FILE_CATEGORY | cut -d "." -f 1)

        echo -n > out/merge/$MAIN_CATEGORY/$CATEGORY.out
        echo -n > error/merge/$MAIN_CATEGORY/$CATEGORY.out

        sbatch -J merge/$MAIN_CATEGORY/$CATEGORY -o out/merge/$MAIN_CATEGORY/$CATEGORY.out -e error/merge/$MAIN_CATEGORY/$CATEGORY.out merge/shell_script/unit_merge.sh -mc $MAIN_CATEGORY -c $CATEGORY
    done
done