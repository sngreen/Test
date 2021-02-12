#!/bin/bash

# delete existing branches

git checkout master    
git branch | grep -v master | while read b
 do 
    git push origin --delete $b
    git branch -D $b
 done

# create new branches

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

# create first commit (at the bottom)

git checkout releases/R5.0K
git pull
git checkout -b fix_K/R5.0K
echo fix_K/R5.0K > file.txt
git commit -am 'fix_K/R5.0K, first commit'
git push --set-upstream origin fix_K/R5.0K
echo create pull request from ix_K/R5.0K to releases/R5.0K

#
#
#

# git checkout releases/R5.0H && git pull && git checkout -b fix_H/R5.0H && echo fix_H/R5.0H >> file.txt && git commit -am 'fix_H/R5.0H, message' && git push --set-upstream origin fix_H/R5.0H