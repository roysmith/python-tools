#!/usr/bin/env python

import argparse
import traceback_helper as helper

def parse_cli():
    parser = argparse.ArgumentParser(description="find and categorize python stack dumps")
    parser.add_argument("input_file")
    return parser.parse_args()

def main(args):
    crashes = {}
    for line in open(args.input_file):
        if '#012' not in line:
            # line doesn't appear to have a stack dump, skip it
            continue
        lines = helper.unfold(line)
        header, stack = helper.extract_stack(lines)
        signature = tuple(stack)
        if signature in crashes:
            count, header = crashes[signature]
            crashes[signature] = (count + 1, header)
        else:
            crashes[signature] = (1, header)

    # We've accumulated all the stack frames and aggregated them by
    # signature.  All that's left is to sort them by signature
    # frequency and print them out.
    crash_list = [(count, header, signature) for signature, (count, header) in crashes.iteritems()]
    crash_list.sort(reverse=True)
    for count, header, signature in crash_list:
        print
        print '%d occurances' % count
        print header
        for frame in signature:
            print "%s:%s()" % frame
        print '========================================'
    
if __name__ == '__main__':
    args = parse_cli()
    main(args)
