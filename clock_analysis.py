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
        "Rising Time (ns)": rising_times,
        "Falling Time (ns)": falling_times,
        "Rising Duty Cycle (%)": rising_duty_cycles,
        "Rising Skew (ns)": rising_skew_times,
        "Jitter (ns)": round(jitter, 2)
    }

    return results

# Function to write results to file
def write_results_to_file(results, filename):
    with open(filename, 'w') as file:
        if results['Average Clock Period (ns)'] is not None:
            file.write(f"Average Clock Period (ns): {results['Average Clock Period (ns)']:.2f}\n")
        
        file.write(f"Rising Time (ns): {[round(time, 2) for time in results['Rising Time (ns)']]}\n")
        file.write(f"Falling Time (ns): {[round(time, 2) for time in results['Falling Time (ns)']]}\n")
        if results['Rising Duty Cycle (%)']:
            file.write(f"Rising Duty Cycle (%): {[round(cycle, 2) for cycle in results['Rising Duty Cycle (%)']]}\n")
        if results['Rising Skew (ns)']:
            file.write(f"Rising Skew (ns): {[round(skew, 2) for skew in results['Rising Skew (ns)']]}\n")
        file.write(f"Jitter (ns): {results['Jitter (ns)']:.2f}\n")

# Main script
if __name__ == "__main__":
    # Simulate random clock generation
    clk_values = simulate_random_clock(simulation_time_ns)

    # Analyze clock behavior
    results = analyze_clock(clk_values)

    # Write results to file
    filename = "clock_analysis_results.txt"
    write_results_to_file(results, filename)

    print(f"Clock analysis results written to '{filename}'")
