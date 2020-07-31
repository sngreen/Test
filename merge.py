#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
# @package    
# @brief      
#
# @version    $Revision: $
# @author     Sergey Green
# @note       
# @note       $Date:     $
# @note       $URL:      $
# @purpose    Create ripple merge from lower branches to master.
# @usage 
#
# add this line to .bashrc
# export GIT_MERGE_AUTOEDIT=no
# source ~/.bashrc

import sys
import os
import json

os.environ['GIT_MERGE_AUTOEDIT'] = 'no'

class AutomaticMerge:
    
    def __init__(self, **kwds):
        
        self.infile = kwds.get('infile')
        self.current_branch = kwds.get('current_branch')

        self.automatic_merge()

    def get_branches(self):

        with open(self.infile) as json_file:
            data = json.load(json_file)

        x = data['merges'].index(self.current_branch)
        return data['merges'][x:]

    def automatic_merge(self):
        
        branches = self.get_branches()
        reset = False

        print('Auto-merging through: {}'.format(' '.join(branches)))
        
        for branch, onto in zip(branches, branches[1:]):
            
            if onto:
                print()
                print('{:12} => {}'.format(branch, onto))

                cmd = 'git checkout {} && git merge refs/heads/{}'.format(onto, branch)
                print('{:12} => {}'.format('cmd', cmd)) 
                
                returned_value = os.system(cmd)
                print('{:12} => {} : {}'.format('merged', branch, returned_value))
                
                if returned_value:
                    print('{:12} => {} : merge failed .. hard reset.'.format(branch, onto))
                   
                    cmd = 'git reset --hard'
                    os.system(cmd) 
                    reset = True

        if reset:
            for onto in branches[1:]:
                cmd = 'git checkout {} && git reset --hard'.format(onto)

                print('{:12} => {:6} failed, reset to original state'.format('Auto-merge', onto))

        else:
            print()
            for onto in branches[1:]:
                cmd = 'git checkout {} && git push origin {}'.format(onto, onto)

                print('{:12} => {:6} finished'.format('Auto-merge', onto))

def main():
    AutomaticMerge(infile='merges.json', current_branch='18500')
    
if __name__ == '__main__':
    main()
