#!/usr/bin/env python3

from __future__ import print_function

from argparse import ArgumentParser, RawTextHelpFormatter
import re
import sys
import json

import vcdvcd
from vcdvcd import VCDVCD
from io import StringIO


def main():
    # Redirect stdout to capture the terminal output
    old_stdout = sys.stdout
    sys.stdout = mystdout = StringIO()

    args = parse_arguments()
    results = process_vcd_file(args)

    # Capture the output from StringIO
    terminal_output = mystdout.getvalue()
    
    # Reset stdout
    sys.stdout = old_stdout

    # Write terminal output to text file
    with open('output_terminal.txt', 'w') as terminal_file:
        terminal_file.write(terminal_output)

    # Write results to JSON file
    output_json_filename = 'output.json'
    results["terminal_output"] = terminal_output
    with open(output_json_filename, 'w') as json_file:
        json.dump(results, json_file, indent=4)
    
    print(f"Output saved to {output_json_filename} and output_terminal.txt")


def parse_arguments():
    parser = ArgumentParser(
        description='Print Verilog value change dump (VCD) files in tabular form.',
        epilog="""
# Examples
...
""",
        formatter_class=RawTextHelpFormatter,
    )
    parser.add_argument(
        '--china',
        action='store_true',
        default=False,
        help='https://github.com/cirosantilli/vcdvcd#china',
    )
    parser.add_argument(
        '-d',
        '--deltas',
        action='store_true',
        default=False,
        help='https://github.com/cirosantilli/vcdvcd#vcdcat-deltas',
    )
    parser.add_argument(
        '-l',
        '--list',
        action='store_true',
        default=False,
        help='list signal names and quit',
    )
    group = parser.add_mutually_exclusive_group()
    group.add_argument(
        '-x',
        '--exact',
        action='store_true',
        default=False,
        help='signal names must match exactly, instead of the default substring match',
    )
    group.add_argument(
        '-r',
        '--regexp',
        action='store_true',
        default=False,
        help='signal names are treated as Python regular expressions',
    )
    parser.add_argument(
        'vcd_path',
        metavar='vcd-path',
        nargs='?',
    )
    parser.add_argument(
        'signals',
        help='only print values for these signals. Substrings of the signal are considered a match by default.',
        metavar='signals',
        nargs='*'
    )
    return parser.parse_args()


def process_vcd_file(args):
    results = {"signals": [], "data": []}
    if args.china:
        results["china"] = vcdvcd.china()
    else:
        vcd = VCDVCD(args.vcd_path, only_sigs=True)
        all_signals = vcd.signals
        if args.signals:
            selected_signals = []
            for s in args.signals:
                r = re.compile(s)
                for a in all_signals:
                    if (
                        (args.regexp and r.search(a)) or
                        (args.exact and s == a) or
                        (not args.exact and s in a)
                    ):
                        selected_signals.append(a)
            signals = selected_signals
        else:
            signals = all_signals

        results["signals"] = signals

        if args.list:
            results["list"] = signals
        else:
            if args.deltas:
                callbacks = vcdvcd.PrintDeltasStreamParserCallbacks()
            else:
                callbacks = vcdvcd.PrintDumpsStreamParserCallbacks()
            vcd_parser = VCDVCD(
                args.vcd_path,
                signals=signals,
                store_tvs=True,
                callbacks=callbacks,
            )
            
            time_values = {}
            for signal in signals:
                for tv in vcd_parser[signal].tv:
                    time, value = tv
                    if time not in time_values:
                        time_values[time] = ["0"] * len(signals)
                    time_values[time][signals.index(signal)] = value

            times = sorted(time_values.keys())
            for time in times:
                values = time_values[time]
                results["data"].append({"time": time, "values": values})

    return results


if __name__ == '__main__':
    main()
