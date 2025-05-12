import subprocess
import time

def get_cpu_usage():
    try:
        def get_cpu_times():
            """Helper function to get CPU times from /proc/stat."""
            stat_output = subprocess.run(['cat', '/proc/stat'], capture_output=True, text=True).stdout.strip()
            for line in stat_output.splitlines():
                if line.startswith('cpu '):  # Note the space after 'cpu'
                    parts = line.split()
                    if len(parts) >= 5:
                        user = int(parts[1])
                        nice = int(parts[2])
                        system = int(parts[3])
                        idle = int(parts[4])
                        iowait = int(parts[5]) if len(parts) > 5 else 0
                        irq = int(parts[6]) if len(parts) > 6 else 0
                        softirq = int(parts[7]) if len(parts) > 7 else 0
                        return user, nice, system, idle, iowait, irq, softirq
                    else:
                        raise ValueError("Invalid /proc/stat format: Not enough values")
            raise ValueError("No 'cpu ' line found in /proc/stat")

        # Get initial CPU times
        cpu_times_1 = get_cpu_times()
        time.sleep(0.1)  # Short delay
        cpu_times_2 = get_cpu_times()

        # Calculate the differences
        user_diff = cpu_times_2[0] - cpu_times_1[0]
        nice_diff = cpu_times_2[1] - cpu_times_1[1]
        system_diff = cpu_times_2[2] - cpu_times_1[2]
        idle_diff = cpu_times_2[3] - cpu_times_1[3]
        iowait_diff = cpu_times_2[4] - cpu_times_1[4]
        irq_diff = cpu_times_2[5] - cpu_times_1[5]
        softirq_diff = cpu_times_2[6] - cpu_times_1[6]

        total_diff = user_diff + nice_diff + system_diff + idle_diff + iowait_diff + irq_diff + softirq_diff

        if total_diff == 0:
            return "0.00%"  # Avoid division by zero
        cpu_usage = (1 - (idle_diff / total_diff)) * 100
        return f"{cpu_usage:.2f}%"
    except Exception as e:
        return f"Error: {e}"    

def get_memory_usage():
    try:
        meminfo_output = subprocess.run(['cat', '/proc/meminfo'], capture_output=True, text=True).stdout.strip()
        mem_data = {}
        for line in meminfo_output.splitlines():
            if ':' in line:
                key, value = line.split(':', 1)
                mem_data[key.strip()] = value.strip().split()[0]  # Get value in KB

        if 'MemTotal' not in mem_data or 'MemAvailable' not in mem_data:
            return "Error: MemTotal or MemAvailable not found in /proc/meminfo"

        total_kb = float(mem_data['MemTotal'])
        available_kb = float(mem_data['MemAvailable'])
        used_kb = total_kb - available_kb

        percent = (used_kb / total_kb) * 100
        total_gb = total_kb / 1024 / 1024
        available_gb = available_kb / 1024 / 1024

        return f"{percent:.2f}% ({available_gb:.2f} GB free / {total_gb:.2f} GB total)"
    except Exception as e:
        return f"Error: {e}"

def get_disk_usage(disk_path="/"):
    try:
        df_output = subprocess.run(['df', '-h', disk_path], capture_output=True, text=True).stdout.strip().splitlines()
        if len(df_output) < 2:
            return "Error: Could not retrieve disk information."
        parts = df_output[1].split()
        if len(parts) < 5:
            return "Error: Incomplete disk information."
        total = parts[1]
        used = parts[2]
        available = parts[3]
        percent = parts[4]
        return f"{percent} ({available} free / {total} total)"
    except Exception as e:
        return f"Error: {e}"

def get_network_stats(interface="eth0"):
    try:
        net_dev_output = subprocess.run(['awk', f'/{interface}/{{print $2, $10}}', '/proc/net/dev'], capture_output=True, text=True).stdout.strip()
        if not net_dev_output:
            return f"Error: Interface {interface} not found"
        parts = net_dev_output.split()

        if len(parts) < 2:
           return "Error: Incomplete network information"
        rx_bytes_initial, tx_bytes_initial = map(float, parts)

        time.sleep(2)
        net_dev_output = subprocess.run(['awk', f'/{interface}/{{print $2, $10}}', '/proc/net/dev'], capture_output=True, text=True).stdout.strip()
        parts = net_dev_output.split()
        if len(parts) < 2:
            return "Error: Incomplete network information after sleep"
        rx_bytes_final, tx_bytes_final = map(float, parts)

        rx_diff = rx_bytes_final - rx_bytes_initial
        tx_diff = tx_bytes_final - tx_bytes_initial
        rx_mb_s = (rx_diff / 1024 / 1024) / 2
        tx_mb_s = (tx_diff / 1024 / 1024) / 2
        return f"Sent: {tx_mb_s:.2f} MB/s, Received: {rx_mb_s:.2f} MB/s"
    except Exception as e:
        return f"Error: {e}"

def get_uptime():
    try:
        uptime_seconds = float(subprocess.run(['cat', '/proc/uptime'], capture_output=True, text=True).stdout.strip().split()[0])
        days = int(uptime_seconds // 86400)
        hours = int((uptime_seconds % 86400) // 3600)
        minutes = int((uptime_seconds % 3600) // 60)
        seconds = int(uptime_seconds % 60)
        return f"{days} days, {hours} hours, {minutes} minutes, {seconds} seconds"
    except Exception as e:
        return f"Error: {e}"

if __name__ == '__main__':
   print(get_cpu_usage())
   print(get_memory_usage())
   print(get_disk_usage())
   print(get_network_stats())
   print(get_uptime())
