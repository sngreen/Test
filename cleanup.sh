#!/bin/bash

git checkout master    
git branch | grep -v master | while read name
 do 
    git push origin --delete $name
    git branch -D $name
 done
 
cat branches.txt  | while read b
do 
    git checkout -b $b
    u=$(echo $b | sed -e 'sa/a_a')
    echo $b > ${u}.txt
    echo 222222222222222 > file_2.txt
    git add --all
    git commit -am 'added two files'
    git push --set-upstream origin $b
    git checkout master
done
