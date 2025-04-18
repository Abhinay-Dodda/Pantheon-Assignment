#!/usr/bin/env python2
# -*- coding: utf-8 -*-
import matplotlib
matplotlib.use('Agg')
import os
import argparse
import matplotlib.pyplot as plt


def parse_stats_file(filepath):
    rtt_avg = None
    rtt_95 = None
    throughput = None
    with open(filepath) as f:
        for line in f:
            if 'average RTT' in line:
                rtt_avg = float(line.strip().split()[-2])  # ms
            if '95th percentile RTT' in line:
                rtt_95 = float(line.strip().split()[-2])  # ms
            if 'throughput' in line and 'recv' in line:
                throughput = float(line.strip().split()[-2])  # Mbps
    return rtt_avg, rtt_95, throughput


def plot_rtt_vs_throughput(scheme_data, output_path, rtt_type='avg'):
    plt.figure()
    for scheme, stats in scheme_data.items():
        rtt, throughput = stats[rtt_type], stats['throughput']
        if rtt is None or throughput is None:
            continue
        plt.scatter(rtt, throughput, label=scheme)
        plt.text(rtt, throughput, scheme, fontsize=9, ha='right')

    plt.xlabel("RTT (ms)")
    plt.ylabel("Throughput (Mbps)")
    plt.title("RTT vs Throughput ({})".format(rtt_type))
    plt.grid(True)
    plt.gca().invert_xaxis()  # Higher RTT closer to origin
    plt.tight_layout()
    plt.savefig(output_path)
    plt.close()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True, help="Folder with *_stats_run1.log files")
    parser.add_argument("--schemes", required=True, help="Space-separated list of CC schemes")
    parser.add_argument("--rtt", default="avg", choices=["avg", "95"], help="RTT metric to use on x-axis")
    args = parser.parse_args()

    scheme_data = {}
    for scheme in args.schemes.split():
        filepath = os.path.join(args.input, "{}_stats_run1.log".format(scheme))
        if not os.path.exists(filepath):
            print("[!] Stats file not found for scheme: {}".format(scheme))
            continue
        rtt_avg, rtt_95, throughput = parse_stats_file(filepath)
        scheme_data[scheme] = {
            'avg': rtt_avg,
            '95': rtt_95,
            'throughput': throughput
        }

    if scheme_data:
        output_file = os.path.join(args.input, "rtt_vs_throughput_{}.png".format(args.rtt))
        plot_rtt_vs_throughput(scheme_data, output_file, rtt_type=args.rtt)
        print("[+] RTT vs Throughput plot saved as: {}".format(output_file))
    else:
        print("[!] No valid scheme data to plot.")


if __name__ == '__main__':
    main()
