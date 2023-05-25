#!/bin/sh


while getopts t:p:f: flag
do
    case "${flag}" in
        t) time=${OPTARG};;
        p) path=${OPTARG};;
        f) prefix=${OPTARG};;
    esac
done
echo "time: $time";
echo "path: $path";
echo "Prefix:: $prefix";



json -I -f package.json -e "this.name='adar'"
