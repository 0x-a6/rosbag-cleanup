#!/usr/bin/env python
from ast import parse
import sys
import roslib;
import rospy
import rosbag
from rospy import rostime
import argparse
import os

''' 
Bag Merge for python 3
Designed for combining anynumber of python bags
Reindexing time to be continuous
'''

class Bag:
    '''
    Bag Class to store location and details about the bag
    '''

def parse_args():
    parser = argparse.ArgumentParser(
        prog = 'bm3.py',
        description='Merges bagfiles.')
    parser.add_argument('-o', type=str, help='name of the output file', 
        default = None, metavar = "output_file")
    parser.add_argument('-t', type=str, help='topics which should be merged to the main bag', 
        default = None, metavar = "topics")
    parser.add_argument('-i', help='reindex bagfile', 
        default = False, action="store_true")
    parser.add_argument('bagfile', type=str, help='path to a bagfile which should be merged to the main bagfile')
    args = parser.parse_args()
    return args

if __name__ == "__main__":
    args = parse_args()
    args.t = args.t.split(',') if args.t != None else args.t
    
