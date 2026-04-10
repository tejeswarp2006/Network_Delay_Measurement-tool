import subprocess
import re
import statistics
import platform

def measure_latency(host, count=10):
    param = '-n' if platform.system().lower() == 'windows' else '-c'
    command = ['ping', param, str(count), host]

    try:
        output = subprocess.check_output(command, universal_newlines=True)
        rtt_matches = re.findall(r'time[=<]([0-9\.]+)\s*ms', output)
        rtt_values = [float(match) for match in rtt_matches]
        return rtt_values if rtt_values else None
    except subprocess.CalledProcessError:
        return None

def analyze_delays(hosts):
    results = {}
    for host in hosts:
        print(f"Measuring path to {host}...")
        rtt_values = measure_latency(host, count=10)

        if rtt_values:
            avg_rtt = statistics.mean(rtt_values)
            min_rtt = min(rtt_values)
            max_rtt = max(rtt_values)
            jitter = statistics.stdev(rtt_values) if len(rtt_values) > 1 else 0

            results[host] = {
                'rtt_values': rtt_values,
                'avg': avg_rtt,
                'min': min_rtt,
                'max': max_rtt,
                'jitter': jitter
            }
        else:
            print(f"[-] Failed to reach {host}")

    return results

if __name__ == "__main__":
    # Mininet host IPs
    target_hosts = [
        '10.0.0.2',  # h2
        '10.0.0.3'   # h3
    ]

    print("Initiating Network Delay Measurement...\n")
    analysis_report = analyze_delays(target_hosts)

    print("\n" + "="*40)
    print("      NETWORK DELAY ANALYSIS REPORT")
    print("="*40)

    for host, stats in analysis_report.items():
        print(f"\nTarget Host: {host}")
        print(f"  --> Raw RTTs (ms) : {stats['rtt_values']}")
        print(f"  --> Minimum Delay : {stats['min']} ms")
        print(f"  --> Maximum Delay : {stats['max']} ms")
        print(f"  --> Average Latency: {stats['avg']:.2f} ms")
        print(f"  --> Jitter (StdDev): {stats['jitter']:.2f} ms")
        print("-" * 40)
