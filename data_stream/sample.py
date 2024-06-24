import pyverilog.vcd.vcdreader as vcdreader
import numpy as np

def extract_timing_info(vcd_file, signal_name, output_file):
    reader = vcdreader.VCDReader(vcd_file)
    timescale = reader.timescale
    signal_data = reader.get_data()[signal_name]

    # Initialize lists to store timing info
    rising_times = []
    falling_times = []
    previous_value = None

    for timestamp, value in signal_data:
        if previous_value is not None:
            if value == '1' and previous_value == '0':
                rising_times.append(timestamp)
            elif value == '0' and previous_value == '1':
                falling_times.append(timestamp)
        previous_value = value

    rising_times = np.array(rising_times, dtype=float)
    falling_times = np.array(falling_times, dtype=float)

    # Calculate metrics
    rise_times = np.diff(rising_times)
    fall_times = np.diff(falling_times)
    skew = np.mean(rise_times) - np.mean(fall_times)
    jitter = np.std(rise_times)

    # Assume data is incrementing if average rise time is smaller than average fall time
    incrementing = np.mean(rise_times) < np.mean(fall_times)

    # Calculate delay and pulse shift
    delay = np.mean(rise_times)
    pulse_shift = rising_times - falling_times[:len(rising_times)]

    # Write details to output file
    with open(output_file, 'w') as f:
        f.write(f"Rising Times: {rising_times.tolist()}\n")
        f.write(f"Falling Times: {falling_times.tolist()}\n")
        f.write(f"Skew: {skew}\n")
        f.write(f"Jitter: {jitter}\n")
        f.write(f"Incrementing: {incrementing}\n")
        f.write(f"Delay: {delay}\n")
        f.write(f"Pulse Shift: {pulse_shift.tolist()}\n")

if __name__ == "__main__":
    vcd_file = 'data_stream.vcd'
    signal_name = 'testbench.uut.data_out'
    output_file = 'timing_info.txt'
    extract_timing_info(vcd_file, signal_name, output_file)
