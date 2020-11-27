#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# @package    
# @brief      
#
# @version    $Revision: $
# @author     Sergey Green
# @note       (c) 
# @note       $Date:     $
# @note       $URL:      $
#
#
import sys
import re
import logging
from argparse import ArgumentParser, RawTextHelpFormatter

formatter = logging.Formatter('%(message)s')
console = logging.StreamHandler()
console.setFormatter(formatter)

LOGGER = logging.getLogger(__name__)
LOGGER.addHandler(console)
LOGGER.setLevel(2)

# 18505
# SCMTEST-7
# python3 verify_message.py --branch 18505 --commit cda17c84e50fe16c5db78acb93f567ae2d3d856c --message 'wrote 0 to a file'
# message [SEGR] AZPDEVOPS-5253 Wrote 1 to a file
# 'wrote 0 to a file' is not a propper commit-message (push aborted) ...
# error: failed to push some refs to 'https://github.com/sngreen/Test.git'
# scm@LX-EMWP06:~/Projects/repositories/Test$ git push
# warning: url has no scheme: username=sngreen
# fatal: credential url cannot be parsed: username=sngreen
# .git/hooks/pre-push: 11: function: not found
# origin
# .git/hooks/pre-push: 15: Syntax error: "}" unexpected
# error: failed to push some refs to 'https://github.com/sngreen/Test.git'

class CommitMsg:

    def __init__(self):
        
        # declarations
        self.format = '{0:<12} : {1:<1}'
        self.pattern ='\[[A-Z]{4}\]\s[A-Z]{5,9}\-[0-9]{1,5}\s\w+'

        # methods  
        self.collect_args()
        self.print_format()
       
    def collect_args(self):
        
        parser = ArgumentParser(
            formatter_class=RawTextHelpFormatter,
            description='Script to verify the commit-message.'
        )

        parser.add_argument('--branch',
            required= True,
            default = None,
            help='Branch of where the commit was done. \nThis parameter is required.\ndefault: %(default)s',
        )

        parser.add_argument('--commit',
            required= True,
            default = None,
            help='Commit sha1. \nThis parameter is required. \ndefault: %(default)s',
        )

        parser.add_argument('--message',
            required= True,
            default =None,
            help='Commit message. \nThis paremeter is required. \ndefault: %(default)s',
        )
        
        self.args = parser.parse_args()

    def print_format(self):

        propper = '''
{0}
Branch  : {1}
Commit  : {2}    
Message :'{3}'



Please update your commit-message (git rebase -i HEAD~N) to this format;

[ABCD]          - First two letters of your first name + first two letters of your last name
AZPXXXXXX-12345 - Jira ticket
Commit message  - What was done ..

Example 
[ABCD] AZPXXXXXX-12345 Commit message ..

git log --pretty=oneline | head -10 => will show where the offending commit is.
git rebase -i HEAD~N                => N commits to look at.

{0}
        '''.format('-'*77, self.args.branch,self.args.commit, self.args.message.replace('\n','\n\t  '))

        LOGGER.info(propper)
       
def main():
    CommitMsg()

if __name__ == '__main__':
    main() 
