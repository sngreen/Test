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
#
#
import sys
import time
import logging

formatter = logging.Formatter('%(asctime)s : %(name)s : %(message)s', datefmt='%Y-%m-%d %I:%M:%S %p')

handler = logging.FileHandler('file1.log')
handler.setFormatter(formatter)

LOGGER = logging.getLogger(__name__)
LOGGER.addHandler(handler)
LOGGER.setLevel(2)

class LoggingExample:
    def __init__(self):

        # methods
        self.say_hello()
        self.change_logger()
        self.say_hello()
    
    def say_hello(self):

        LOGGER.info(sys._getframe().f_code.co_name)
        print('Hello to the logger')

    def change_logger(self):

        LOGGER.handlers = [] 
        handler = logging.FileHandler('file2.log')
        handler.setFormatter(formatter)
        LOGGER.addHandler(handler)

        time.sleep(3)
        
def main():
    LoggingExample()
   
if __name__ == '__main__':
    main()
