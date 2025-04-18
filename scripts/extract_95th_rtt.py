#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import os
import argparse
import numpy as np

def extract_rtt(log_file):
    rtts = []
    with open(log_file) as f:
        for line in f:
            parts = line.strip().split('\t')
            if len(parts) != 3:
                continue
            timestamp, event_type, rtt = parts
            if event_type == 'r':  # 'r' means RTT sample recorded
                try:
                    rtts.append(float(rtt))
                except:
                    continue
    return rtts

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True, help="Input folder with *_datalink_run1.log files")
    parser.add_argument("--schemes", required=True, help="Space-separated list of schemes")
    args = parser.parse_args()

    for scheme in args.schemes.split():
        file_path = os.path.join(args.input, "{}_datalink_run1.log".format(scheme))
        if not os.path.exists(file_path):
            print("[!] Missing file: {}".format(file_path))
            continue
        rtts = extract_rtt(file_path)
        if rtts:
            p95 = np.percentile(rtts, 95)
            avg = np.mean(rtts)
            print("{}: avg RTT = {:.2f} ms, 95th percentile RTT = {:.2f} ms".format(scheme, avg, p95))
        else:
            print("{}: No RTT data found.".format(scheme))

if __name__ == '__main__':
    main()
