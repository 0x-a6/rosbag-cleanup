#!/usr/bin/env python3
from ast import parse
import rosbag
import time
from rosbag import ROSBagException
from rospy import rostime
import argparse
import os
import re

''' 
Bag Merge for python 3
Designed for combining anynumber of ROS bags
Reindexing time to be continuous
'''

def parse_args() -> None:
    parser = argparse.ArgumentParser(
        prog = 'bm3.py',
        description='Merges bagfiles.')
    parser.add_argument('-o', type=str, help='name of the output file', 
        default = None, metavar = "output_file")
    parser.add_argument('bagfiles', nargs='+', help='path to a bagfile which should be merged to the main bagfile')
    args = parser.parse_args()

    full_paths = [os.path.join(os.getcwd(), path) for path in args.bagfiles]

    args.bagfiles = set()
    for path in full_paths:
        if os.path.isfile(path):
            args.bagfiles.add(path)
    return args

class Bag():
    '''
    Bag Class
        @start = rostime start of the ROS bag
        @stop = rostime stop of the ROS bag
        @data = rosbag.Bag Object
        optional @path = name of the ROS bag
    '''
    def __init__(self, data, path = None) -> None:
        self.path = path
        self.data = data
        self.start = rostime.Time(int(time.time()))
        self.stop = rostime.Time(0)

    def __str__(self) -> str:
        return f'Name: {self.path}\nStart: {time.ctime(self.start.secs)}, Stop: {time.ctime(self.stop.secs)}'

def ingest_bag(path) -> Bag:
    bag = Bag(rosbag.Bag(path), path)
    for topic, msg, bag_time in bag.data.read_messages():
        if bag.start == None or bag_time < bag.start:
            bag.start = bag_time
        if bag.stop == None or bag_time > bag.stop:
            bag.stop = bag_time
    return bag

def get_next(it, offset) -> tuple:
    try:
        next_step = next(it)
        return (next_step[0], next_step[1], next_step[2] - offset)
    except StopIteration: 
        return None

def merge_bag(bagfiles, outfile=None) -> None:
    # ingest bag data
    bags = []
    for bag_path in bagfiles:
        try:
            print(f'Digesting: {os.path.basename(bag_path)}')
            bags.append(ingest_bag(bag_path))
        except ROSBagException:
            pass # ignore any files that aren't ROS bags

    if len(bags) < 2:
        raise ValueError("Not enough bag files to merge")

    # sort bags on start date
    bags.sort(key=lambda x:x.start)

    index = 0
    outfile = f'{bags[0].path}_merged_{index}.bag' if outfile == None else f'{outfile}'

    while (os.path.exists(f'{outfile}')):
        outfile = re.sub('_merged_[0-9]*', f'_merged_{index}', outfile)
        index += 1
    
    # #merge bagfile
    outbag = rosbag.Bag(outfile, 'w')
    time_offset = bags[0].start # zero offset for first bag
    try:
        for bag in bags:
            time_offset = bag.start - time_offset # start of this bag - end of last bag
            bag_it = bag.data.__iter__()
            bag_next = get_next(bag_it, time_offset)
            while bag_next != None:
                outbag.write(bag_next[0], bag_next[1], bag_next[2])
                bag_next = get_next(bag_it, time_offset)
            time_offset = bag.stop # end of this bag
    finally:
        outbag.close()

if __name__ == "__main__":
    args = parse_args()
    merge_bag(args.bagfiles, outfile=args.outfile)

    
