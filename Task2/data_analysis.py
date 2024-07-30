import json
import numpy as np
from scipy import stats

def analyze_data(json_file):
    with open(json_file, 'r') as f:
        data = json.load(f)
    
    signal_data = extract_signal_data(data)
    analysis_results = {}

    analysis_results['incremental_decremental'] = analyze_incremental_decremental(signal_data)
    analysis_results['pulse_shift'] = analyze_pulse_shift(signal_data)
    analysis_results['frequency'] = analyze_frequency(signal_data)
    analysis_results['duty_cycle'] = analyze_duty_cycle(signal_data)
    analysis_results['correlation'] = analyze_correlation(signal_data)
    analysis_results['overlap'] = analyze_signal_overlap(signal_data)

    # Convert numpy types to native Python types
    analysis_results = convert_numpy_types(analysis_results)

    #with open('analysis_results.json', 'w') as f:
        #json.dump(analysis_results, f, indent=4)
    output_filename = "data_analysis.txt"
    with open(output_filename, 'w') as f:
        f.write("Incremental/Decremental Analysis:\n")
        for signal, result in analysis_results['incremental_decremental'].items():
            f.write(f"  {signal}: {result}\n")
        f.write("\nPulse Shift Analysis:\n")
        for signal, shifts in analysis_results['pulse_shift'].items():
            f.write(f"  {signal}:\n")
            f.write(f"    Positive Shifts: {shifts['positive_shifts']}\n")
            f.write(f"    Negative Shifts: {shifts['negative_shifts']}\n")
        f.write("\nFrequency Analysis:\n")
        for signal, freq in analysis_results['frequency'].items():
            f.write(f"  {signal}: {freq} Hz\n")
        f.write("\nDuty Cycle Analysis:\n")
        for signal, duty in analysis_results['duty_cycle'].items():
            f.write(f"  {signal}: {duty:.6f}\n")
        f.write("\nCorrelation Analysis:\n")
        f.write(f"  Correlation: {analysis_results['correlation']}\n")
        f.write("\nSignal Overlap Analysis:\n")
        for signal_pair, overlap in analysis_results['overlap'].items():
            f.write(f"  {signal_pair}: {overlap}\n")

    
    print(f"Data analysis saved to {output_filename}")

def convert_numpy_types(data):
    if isinstance(data, dict):
        return {key: convert_numpy_types(value) for key, value in data.items()}
    elif isinstance(data, list):
        return [convert_numpy_types(item) for item in data]
    elif isinstance(data, (np.integer, np.floating)):
        return data.item()
    else:
        return data

def extract_signal_data(data):
    signal_data = {}
    for entry in data['data']:
        time = entry['time']
        values = entry['values']
        for i, signal in enumerate(data['signals']):
            if signal not in signal_data:
                signal_data[signal] = []
            signal_data[signal].append(values[i])
    return signal_data

def convert_to_numeric(values):
    numeric_values = []
    for v in values:
        try:
            numeric_values.append(float(v))
        except ValueError:
            # Handle non-numeric values (like 'x')
            numeric_values.append(0)  # or 1, based on your preference
    return numeric_values

def analyze_incremental_decremental(signal_data):
    results = {}
    for signal, values in signal_data.items():
        try:
            numeric_values = convert_to_numeric(values)
            # Remove leading and trailing zeros
            numeric_values = [v for v in numeric_values if v != 0]
            if all(x < y for x, y in zip(numeric_values, numeric_values[1:])):
                results[signal] = 'incremental'
            elif all(x > y for x, y in zip(numeric_values, numeric_values[1:])):
                results[signal] = 'decremental'
            else:
                results[signal] = {
                    'classification': 'neither',
                    'values': numeric_values
                }
        except ValueError:
            results[signal] = {
                'classification': 'non-numeric',
                'values': values
            }
    return results

def analyze_pulse_shift(signal_data):
    results = {}
    for signal, values in signal_data.items():
        try:
            numeric_values = np.array(convert_to_numeric(values))
            transitions = np.diff(numeric_values)
            positive_transitions = transitions[transitions > 0]
            negative_transitions = transitions[transitions < 0]
            results[signal] = {
                'positive_shifts': len(positive_transitions),
                'negative_shifts': len(negative_transitions)
            }
        except ValueError:
            results[signal] = 'non-numeric'
    return results

def analyze_frequency(signal_data):
    results = {}
    for signal, values in signal_data.items():
        try:
            numeric_values = np.array(convert_to_numeric(values))
            zero_crossings = np.where(np.diff(np.signbit(numeric_values)))[0]
            frequency = len(zero_crossings) / (len(numeric_values) - 1)
            results[signal] = frequency
        except ValueError:
            results[signal] = 'non-numeric'
    return results

def analyze_duty_cycle(signal_data):
    results = {}
    for signal, values in signal_data.items():
        try:
            numeric_values = np.array(convert_to_numeric(values))
            high_time = np.sum(numeric_values > 0)
            low_time = np.sum(numeric_values <= 0)
            duty_cycle = high_time / (high_time + low_time)
            results[signal] = duty_cycle
        except ValueError:
            results[signal] = 'non-numeric'
    return results

def analyze_correlation(signal_data):
    if len(signal_data) < 2:
        return None
    
    signal_names = list(signal_data.keys())
    values1 = signal_data[signal_names[0]]
    values2 = signal_data[signal_names[1]]

    try:
        values1 = convert_to_numeric(values1)
        values2 = convert_to_numeric(values2)
    except ValueError:
        print("Error: Non-numeric values found in signal data.")
        return None

    correlation = stats.pearsonr(values1, values2)[0]
    return correlation

def analyze_signal_overlap(signal_data):
    results = {}
    signals = list(signal_data.keys())
    for i in range(len(signals)):
        for j in range(i + 1, len(signals)):
            signal1 = np.array(convert_to_numeric(signal_data[signals[i]]))
            signal2 = np.array(convert_to_numeric(signal_data[signals[j]]))
            overlap = np.sum((signal1 > 0) & (signal2 > 0))
            results[f"{signals[i]}_{signals[j]}"] = overlap
    return results

if __name__ == '__main__':
    analyze_data('output.json')
    
