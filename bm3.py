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
Designed for combining anynumber of ROS bags
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
    # topic merging ... leaving it here doing nothing with it
    # parser.add_argument('-t', type=str, help='topics which should be merged to the main bag', 
        # default = None, metavar = "topics")
    parser.add_argument('-i', help='reindex bagfile', 
        default = False, action="store_true")
    parser.add_argument('bagfiles', nargs='+', help='path to a bagfile which should be merged to the main bagfile')
    args = parser.parse_args()
    full_paths = [os.path.join(os.getcwd(), path) for path in args.bagfiles]
    args.bagfiles = set()
    for path in full_paths:
        if os.path.isfile(path):
            args.bagfiles.add(path)
    return args

if __name__ == "__main__":
    args = parse_args()
    # topic merging ... leaving it here doing nothing with it
    # args.t = args.t.split(',') if args.t != None else args.t
    
    
    
    for f in args.bagfiles:
        print(f)

    
