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
import requests
import json
import logging
from argparse import ArgumentParser, RawTextHelpFormatter

formatter = logging.Formatter('%(message)s')
console = logging.StreamHandler()
console.setFormatter(formatter)

LOGGER = logging.getLogger(__name__)
LOGGER.addHandler(console)
LOGGER.setLevel(2)

ARGS = {
    'options': {
        'lookup':['issue'],
        'comment':['issue', 'text'], 
        'assign':['issue', 'assignee'],
    }
}

# GET     Obtain information about a resource
# POST    Create a new resource
# PUT     Update a resource
# DELETE  Delete a resource

class JiraApi:

    def __init__(self, **kwds):
        
        # parameters (for testing only!)
        self.user = kwds.get('user')
        self.pswd = kwds.get('pswd')
        self.host = kwds.get('host')

        # jira stuff
        self.baseuri = 'rest/api/2'
        self.issueuri = '{}/issue'.format(self.baseuri)
        self.jqluri = '{}/search?jql='.format(self.baseuri)
        self.projecturi = '{}/project'.format(self.baseuri)
        self.transitions={'To Do': '11', 'In Progress': '21', 'Done': '31'}

        # declarations 
        self.format = '{0:<12} : {1:<1}'
       
        # methods  
        self.collect_args()
        self.verify_args()

    def collect_args(self):
        
        parser = ArgumentParser(
            formatter_class=RawTextHelpFormatter,
            description='Basic Jira operations, such as ticket lookup, status change and re-assignment'
        )

        parser.add_argument('--option',
            choices=['lookup', 'comment', 'assign'],
            required=True,
            help='Operation selector\nThis option is required',
        )
        
        
        parser.add_argument('--issue',
            default=None,
            help='Jira Issue. \nUsed with options: lookup, comment, assign \ndefault: %(default)s',
        )

        parser.add_argument('--text',
            default=None,
            help='Text to add to the comment (requires issue)\nUsed with --option: comment \ndefault: %(default)s',
        )

        parser.add_argument('--assignee',
            default=None,
            help='New assignee (requires issue)\nUsed with --option: assign \ndefault: %(default)s',
        )
        
        self.args = parser.parse_args()

    def verify_args(self):

        missing = [arg for arg in ARGS['options'][self.args.option] if not getattr(self.args, arg)]
        
        if not missing:
            self.create_session()
            self.select_operation()
        
        else:
            LOGGER.info('Missing additional paramters: {}'.format(missing))
            sys.exit(1)

    def select_operation(self):

        options = {
            'lookup': self.get_issue,
            'comment': self.add_comment,
            'assign': self.assign_issue
        }

        options[self.args.option](
            issue_key = self.args.issue, 
            comment = self.args.text, 
            assignee = self.args.assignee)

    def create_session(self):

        self.session = requests.Session()
        self.session.verify = 'False'
        self.session.auth = (self.user, self.pswd) 
        self.session.headers = {
            'Connection' : 'keep-alive',
            'Content-Type' : 'application/json',
            'Accept' : 'application/json',
            'X-Atlassian-Token' : 'no-check'
        }

    def get_issue(self, **kwds):

        url = '{}/{}/{}'.format(self.host,self.issueuri, kwds.get('issue_key'))
    
        r = self.session.get(url)

        if not r.status_code == 200:
            self.show_trace(r.status_code)
            sys.exit()

        self.data = json.loads(r.text)

        self.dump_issue()
  
    def get_by_assignee(self, **kwds):

        url = '{}/{}assignee={}'.format(self.host,self.jqluri, kwds.get('assignee'))

        r = self.session.get(url)

        if not r.status_code == 200:
            self.show_trace(r.status_code)
            sys.exit()

        self.data = json.loads(r.text)

    def create_issue(self, **kwds):

        data = {
            "fields": {
                "project":
                {
                    "id": "10000"
                },
                "summary": kwds.get('summary'),
                "description": kwds.get('description'),
                "issuetype":
                {
                    "name": "Task"
                }
            }
        }
       
        url = '{}/{}'.format(self.host,self.issueuri)        
           
        r = self.session.post(url, data=json.dumps(data))   
            
        if r.status_code != 201:
            LOGGER.info('Issue was not created')
            sys.exit()
        
        i = json.loads(r.text)
        
        # show what was done
        for k, v in {'summary': summary,'description': description,'url': i['self'],'id': i['id'],'key': i['key']}.items():
            LOGGER.info(self.format.format(k, v))
       
    def add_comment(self, **kwds): 

        url = '{}/{}/{}/comment'.format(self.host,self.issueuri, kwds.get('issue_key'))
            
        r = self.session.post(url, data=json.dumps({'body': kwds.get('comment')}))
        
        if not r.status_code == 201:
            LOGGER.info('Comment was not added ..')
            sys.exit()

        # show what was done     
        for k, v in {'url': url, 'issue_key': kwds.get('issue_key'), 'comment': kwds.get('comment')}.items():
            LOGGER.info(self.format.format(k, v))
        
    def assign_issue(self, **kwds):

        data={
            'update': {
                'assignee':[
                    {'set':
                        {
                            'name': kwds.get('assignee')
                        }
                    }
                ]
            }
        }

        url = '{}/{}/{}'.format(self.host, self.issueuri, kwds.get('issue_key'))
            
        r = self.session.put(url,data=json.dumps(data))
        
        if not r.status_code == 204:
            LOGGER.info('Issue was not reassigned')
            sys.exit()

        # show what was done
        for k, v in {'issue_key': kwds.get('issue_key'), 'assignee': kwds.get('assignee')}.items():
            LOGGER.info(self.format.format(k,v ))
        
    def update_issue_status(self, **kwds):

        data={
            'transition':{ 
                'id': self.transitions[kwds.get('transition')] 
            }
        }
             
        url = '{}/{}/{}/transitions?expand=transitions.fields'.format(self.host,self.issueuri, kwds.get('issue_key'))
            
        r = self.session.post(url,data=json.dumps(data))
           
        if not r.status_code == 204:
            LOGGER.info('Issue status was not updated ..')
            sys.exit()

        LOGGER.info('Status of {} was updated to {}'.format(kwds.get('issue_key'), kwds.get('transition')))
                
    def get_project(self, key):
        return key['fields']['project']['name']        

    def get_key(self, key):
        return key['key'] 

    def get_summary(self, key):
        return key['fields']['summary']                
            
    def get_description(self, key):
        return key['fields']['description']            
            
    def get_assignee(self, key):
        try:
            assignee = key['fields']['assignee']['displayName']
        except:
            assignee = "-"
                
        return assignee
            
    def get_priority(self, key):
        return key['fields']['priority']['name']       
            
    def get_component(self, key):

        return key['fields']['components']             
            
    def get_labels(self, key):
        return key['fields']['labels']                 
            
    def get_issue_type(self, key):
        return key['fields']['issuetype']['name']      
            
    def get_versions(self, key):
        return key['fields']['versions']               
            
    def get_status(self, key):
        return key['fields']['status']['name']         
            
    def get_resolution(self, key):
        return key['fields']['resolution']
        
    def get_created(self, key):
        return key['fields']['created']
    
    def get_updated(self, key):
        return key['fields']['updated']
    
    def dump_issue(self):

        def show_fields(key):

            for k, v in {
                'key' : self.get_key(key),
                'project' : self.get_project(key),
                'summary' : self.get_summary(key),
                'description' : self.get_description(key),
                'assignee' : self.get_assignee(key),
                'priority' : self.get_priority(key),
                'issuetype' : self.get_issue_type(key),
                'status' : self.get_status(key),
                'created' : self.get_created(key),
                'updated' : self.get_updated(key) }.items():
        
                LOGGER.info (self.format.format(k,v))

        if "issues" in self.data:
            for key in self.data["issues"]: 
                show_fields(key)
        else: 
            show_fields(self.data)
       
def main():
    JiraApi(user='scm', pswd='scmadm', host='http://192.168.102.134:8080')

if __name__ == '__main__':
    main() 
