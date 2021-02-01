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
    git push --set-upstream origin $b
    git checkout master
done
