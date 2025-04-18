# Pantheon Congestion Control Assignment

This repository contains all experiments, data, scripts, and instructions for comparing congestion control protocols using the Pantheon testbed and Mahimahi network emulator.

## 🔎 Overview
This project evaluates and compares three congestion control (CC) algorithms:
- **BBR**
- **Cubic**
- **Vegas**

All tests were conducted using [Pantheon](https://github.com/StanfordSNR/pantheon), with [Mahimahi](https://github.com/ravinet/mahimahi) for network emulation.

## 🌐 Network Profiles Tested
Two distinct network environments were tested:
1. **High Bandwidth, Low Latency:** 50 Mbps bandwidth, 10 ms RTT
2. **Low Bandwidth, High Latency:** 1 Mbps bandwidth, 200 ms RTT

## 📊 Experiment Configuration
- Duration: **60 seconds** for each run
- Traces: Custom traces created manually using fixed-size packet intervals (6250 for 50 Mbps, 125 for 1 Mbps)
- Tool: Mahimahi + `mm-delay`, `mm-link`
- Logging: Pantheon logs and outputs stored under `output/`

## 📁 Directory Structure
```
Pantheon-Assignment/
├── scripts/                       # Custom analysis scripts (loss, RTT, throughput)
├── tools/                         # Install scripts and pip setup
├── output/                        # Raw data and generated plots (not in Git)
├── results_50mbps_10ms/           # Final selected plots from 50 Mbps scenario
├── results_1mbps_200ms/           # Final selected plots from 1 Mbps scenario
├── results_sample_test/           # Sample run using Pantheon traces
└── results_sample/                # Cleaned version of the primary test outputs
```

## 📊 Graphs Included
Each protocol and network scenario includes:
- **Throughput over time**
- **RTT over time**
- **Combined packet loss over time**
- **RTT vs Throughput scatter plot**

## ⚙️ How to Reproduce the Experiments
### Install Dependencies
```bash
cd pantheon/tools
sudo ./install_deps.sh
```

### Setup Scheme Dependencies
```bash
python2 src/experiments/setup.py --install-deps --schemes "bbr cubic vegas"
```

### Run an Experiment (Example: 50 Mbps / 10 ms RTT)
```bash
python2 src/experiments/test.py local \
  --schemes "bbr cubic vegas" \
  --run-times 1 \
  --runtime 60 \
  --data-dir output/results_50mbps_10ms \
  --uplink-trace output/traces/50mbps.trace \
  --downlink-trace output/traces/50mbps.trace \
  --prepend-mm-cmds "mm-delay 5"
```

### Generate Plots
```bash
python2 src/analysis/analyze.py --data-dir output/results_50mbps_10ms --schemes "bbr cubic vegas"
python2 scripts/plot_loss.py --input output/results_50mbps_10ms --schemes "bbr cubic vegas"
python2 scripts/plot_rtt_vs_throughput.py --input output/results_50mbps_10ms --schemes "bbr cubic vegas" --rtt avg
bash'''

If you have questions, feel free to raise issues on the GitHub repository.
