#!/usr/bin/env python2
# -*- coding: utf-8 -*-
import matplotlib
matplotlib.use('Agg')
import os
import argparse
import matplotlib.pyplot as plt


def parse_log(filepath):
    losses = []
    with open(filepath) as f:
        for line in f:
            parts = line.strip().split('\t')
            if len(parts) != 3:
                continue
            timestamp, event_type, _ = parts
            if event_type == 'l':  # 'l' for loss
                losses.append(float(timestamp))
    return losses


def plot_loss(loss_times, scheme, output_dir):
    if not loss_times:
        print("[!] No losses recorded for {}".format(scheme))
        return

    plt.figure()
    plt.hist(loss_times, bins=100, color='gray', alpha=0.7)
    plt.xlabel("Time (s)")
    plt.ylabel("Loss count")
    plt.title("Loss Over Time - {}".format(scheme))
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, "{}_loss_over_time.png".format(scheme)))
    plt.close()


def plot_combined(all_loss_data, output_dir):
    plt.figure()
    for scheme, loss_times in all_loss_data.items():
        if not loss_times:
            continue
        plt.hist(loss_times, bins=100, alpha=0.6, label=scheme, histtype='step')

    plt.xlabel("Time (s)")
    plt.ylabel("Loss count")
    plt.title("Loss Over Time - All Protocols")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, "combined_loss_over_time.png"))
    plt.close()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True, help="Input results folder")
    parser.add_argument("--schemes", required=True, help="Space-separated list of CC schemes")
    args = parser.parse_args()

    all_loss_data = {}
    for scheme in args.schemes.split():
        path = os.path.join(args.input, "{}_datalink_run1.log".format(scheme))
        if not os.path.isfile(path):
            print("[!] Missing file: {}".format(path))
            continue
        loss_times = parse_log(path)
        all_loss_data[scheme] = loss_times
        plot_loss(loss_times, scheme, args.input)

    plot_combined(all_loss_data, args.input)
    print("[+] Loss plots generated and saved in {}".format(args.input))


if __name__ == "__main__":
    main()
