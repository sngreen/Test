#!/bin/bash

git branch | grep -v master | while read b
do
    git checkout $b
    git pull
    echo > file.txt
    git commit -am -
    git commit --allow-empty -am -
    git push
done
    
