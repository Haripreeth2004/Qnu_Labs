#!/usr/bin/env python3

import argparse
import json

def read_json_file(filename):
    with open(filename, 'r') as file:
        return json.load(file)

def find_clock_signals(data, keyword="clock"):
    return [signal for signal in data["signals"] if keyword in signal.lower()]

def analyze_clock(signal_name, time_values):
    rising_edges = []
    falling_edges = []
    last_value = "0"
    last_time = 0

    for entry in time_values:
        time = entry["time"]
        value = entry["values"][signal_name]

        if value == "1" and last_value == "0":
            rising_edges.append(time)
        elif value == "0" and last_value == "1":
            falling_edges.append(time)
        
        last_value = value
        last_time = time

    if len(rising_edges) < 2:
        raise ValueError(f"Not enough rising edges to analyze clock {signal_name}")

    periods = [rising_edges[i] - rising_edges[i-1] for i in range(1, len(rising_edges))]
    duty_cycles = [(falling_edges[i] - rising_edges[i], periods[i]) for i in range(min(len(falling_edges), len(periods)))]

    jitter = max(periods) - min(periods)
    average_period = sum(periods) / len(periods)
    average_duty_cycle = sum(dc[0] for dc in duty_cycles) / sum(dc[1] for dc in duty_cycles)

    return {
        "rising_edges": rising_edges,
        "falling_edges": falling_edges,
        "periods": periods,
        "jitter": jitter,
        "average_period": average_period,
        "duty_cycle": average_duty_cycle,
    }

def calculate_skew(signal1_results, signal2_results):
    skew = []
    for edge1 in signal1_results["rising_edges"]:
        nearest_time = min(signal2_results["rising_edges"], key=lambda x: abs(x - edge1))
        skew.append(nearest_time - edge1)
    return skew

def main():
    input_filename = "output.json"
    output_filename = "clock_analysis.txt"
    parser = argparse.ArgumentParser(description='Analyze clock signals and skew', formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('signal1', metavar='signal1', type=str, help='First clock signal name')
    parser.add_argument('signal2', metavar='signal2', type=str, nargs='?', default=None, help='Second clock signal name (optional)')

    args = parser.parse_args()

    # Read the JSON file
    data = read_json_file(input_filename)

    # Find clock signals
    clock_signals = find_clock_signals(data)

    # Analyze each clock signal
    analysis_results = {}
    for clock in clock_signals:
        index = data["signals"].index(clock)
        time_values = [
            {"time": entry["time"], "values": {clock: entry["values"][index]}}
            for entry in data["data"]
        ]
        analysis_results[clock] = analyze_clock(clock, time_values)
    
    # Write results to a text file
    with open(output_filename, 'w') as file:
        for clock, results in analysis_results.items():
            file.write(f"Analysis for {clock}:\n")
            file.write(f"  Rising Edges: {results['rising_edges']}\n")
            file.write(f"  Falling Edges: {results['falling_edges']}\n")
            file.write(f"  Periods: {results['periods']}\n")
            file.write(f"  Jitter: {results['jitter']} units\n")
            file.write(f"  Average Period: {results['average_period']} units\n")
            file.write(f"  Duty Cycle: {results['duty_cycle'] * 100:.2f}%\n\n")
            
        # Calculate skew if both signal1 and signal2 are provided
        if args.signal2 and args.signal1 in analysis_results and args.signal2 in analysis_results:
            skew_values = calculate_skew(analysis_results[args.signal1], analysis_results[args.signal2])
            file.write(f"Skew Analysis between {args.signal1} and {args.signal2}:\n")
            file.write("Rising Edge Skew:\n")
            for i, skew in enumerate(skew_values):
                file.write(f"  Edge {i+1}: {skew} units\n")
    
    print(f"Clock analysis saved to {output_filename}")

if __name__ == "__main__":
    main()
