import random
import statistics

# Random seed for reproducibility (optional)
random.seed(12345)

# Simulation parameters
simulation_time_ns = 100  # Simulation time in nanoseconds

# Function to simulate random clock generation
def simulate_random_clock(simulation_time_ns):
    clk_values = []
    current_time = 0

    # Start with a rising edge at time zero
    clk_values.append((0, 1))

    while current_time < simulation_time_ns:
        # Generate random delays for rising and falling edges separately
        delay_rising = random.randint(5, 15)
        delay_falling = random.randint(5, 15)

        # Advance time for rising edge
        current_time += delay_rising
        clk_values.append((current_time, 0))  # Rising edge

        if current_time >= simulation_time_ns:
            break

        # Advance time for falling edge
        current_time += delay_falling
        clk_values.append((current_time, 1))  # Falling edge

    return clk_values

# Function to simulate data stream based on the RTL module
def simulate_data_stream(clk_values):
    counter = 0
    data_stream = []
    for time, clk in clk_values:
        if clk == 0:  # Rising edge
            counter += 1
        data_stream.append((time, counter))  # Store the entire counter value
    return data_stream

# Function to analyze clock behavior
def analyze_clock(clk_values):
    periods = []
    rising_times = []
    falling_times = []
    rising_duty_cycles = []
    rising_skew_times = []

    last_rising_edge = None
    last_falling_edge = None

    for time, value in clk_values:
        if value == 1:  # Falling edge
            if last_falling_edge is not None:
                falling_times.append(time)
            last_falling_edge = time

        elif value == 0:  # Rising edge
            rising_times.append(time)
            if last_rising_edge is not None:
                period = time - last_rising_edge
                periods.append(period)
                if last_falling_edge is not None:
                    high_time = last_falling_edge - last_rising_edge
                    duty_cycle = (high_time / period) * 100
                    rising_duty_cycles.append(duty_cycle)
                    expected_falling_edge = last_rising_edge + (period / 2)
                    skew = last_falling_edge - expected_falling_edge
                    rising_skew_times.append(skew)
            last_rising_edge = time

    jitter = statistics.stdev(periods) if len(periods) > 1 else 0

    results = {
        "Average Clock Period (ns)": round(statistics.mean(periods), 2) if periods else None,
        "Jitter (ns)": round(jitter, 2),
        "Rising Times (ns)": rising_times,
        "Falling Times (ns)": falling_times,
        "Rising Duty Cycle (%)": rising_duty_cycles,
        "Rising Skew (ns)": rising_skew_times
    }

    return results

# Function to analyze data stream
def analyze_data_stream(data_stream):
    rising_edges = [time for time, value in data_stream if value == 0]
    falling_edges = [time for time, value in data_stream if value == 1]

    pulse_shifts = [falling_edges[i] - rising_edges[i] for i in range(min(len(rising_edges), len(falling_edges)))]
    delays = [pulse_shifts[i] - pulse_shifts[i-1] for i in range(1, len(pulse_shifts))]

    # Determine if data stream is incrementing or decrementing
    is_incrementing = all(data_stream[i][1] <= data_stream[i+1][1] for i in range(len(data_stream) - 1))
    is_decrementing = all(data_stream[i][1] >= data_stream[i+1][1] for i in range(len(data_stream) - 1))

    # Calculate skew
    rising_skew_times = [falling - rising for rising, falling in zip(rising_edges, falling_edges)]

    results = {
        "Rising Edges (ns)": rising_edges,
        "Falling Edges (ns)": falling_edges,
        "Pulse Shifts (ns)": pulse_shifts,
        "Delays (ns)": delays,
        "Incrementing": is_incrementing,
        "Decrementing": is_decrementing,
        "Rising Skew (ns)": rising_skew_times
    }

    return results

# Function to write results to file
def write_results_to_file(clock_results, data_results, filename):
    with open(filename, 'w') as file:
        file.write("Clock Analysis:\n")
        file.write(f"Average Clock Period (ns): {clock_results['Average Clock Period (ns)']}\n")
        file.write(f"Jitter (ns): {clock_results['Jitter (ns)']}\n")
        file.write(f"Rising Times (ns): {clock_results['Rising Times (ns)']}\n")
        file.write(f"Falling Times (ns): {clock_results['Falling Times (ns)']}\n")
        file.write(f"Rising Duty Cycle (%): {clock_results['Rising Duty Cycle (%)']}\n")
        file.write(f"Rising Skew (ns): {clock_results['Rising Skew (ns)']}\n\n")

        file.write("Data Stream Analysis:\n")
        file.write(f"Rising Edges (ns): {data_results['Rising Edges (ns)']}\n")
        file.write(f"Falling Edges (ns): {data_results['Falling Edges (ns)']}\n")
        file.write(f"Pulse Shifts (ns): {data_results['Pulse Shifts (ns)']}\n")
        file.write(f"Delays (ns): {data_results['Delays (ns)']}\n")
        file.write(f"Incrementing: {data_results['Incrementing']}\n")
        file.write(f"Decrementing: {data_results['Decrementing']}\n")
        file.write(f"Rising Skew (ns): {data_results['Rising Skew (ns)']}\n")

# Main script
if __name__ == "__main__":
    # Simulate random clock generation
    clk_values = simulate_random_clock(simulation_time_ns)

    # Analyze clock behavior
    clock_results = analyze_clock(clk_values)

    # Simulate data stream
    data_stream = simulate_data_stream(clk_values)

    # Analyze data stream
    data_results = analyze_data_stream(data_stream)

    # Write results to file
    filename = "hp_data_stream_analysis_results.txt"
    write_results_to_file(clock_results, data_results, filename)

    print(f"Data stream analysis results written to '{filename}'")
