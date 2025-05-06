#!/bin/bash

# Configuration
UPDATE_INTERVAL=2  # Seconds
NETWORK_INTERFACE="eth0"
DISK_PATH="/"

# Function to clear the screen
clear_screen() {
  clear
}

# Function to get CPU usage
get_cpu_usage() {
  local cpu_idle=$(awk '/^cpu/{print $5}' /proc/stat)
  sleep 0.1 # Small delay to get a second reading
  local cpu_idle_new=$(awk '/^cpu/{print $5}' /proc/stat)
  local cpu_total_diff=$(awk '/^cpu/{total=0; for(i=2; i<=NF; i++) total += $i; print total}' /proc/stat)
  local cpu_total_diff_new=$(awk '/^cpu/{total=0; for(i=2; i<=NF; i++) total += $i; print total}' /proc/stat)
  local idle_diff=$((cpu_idle_new - cpu_idle))
  local total_diff=$((cpu_total_diff_new - cpu_total_diff))
  local cpu_usage=$(echo "scale=2; (1 - ($idle_diff / $total_diff)) * 100" | bc)
  echo "${cpu_usage}%"
}

# Function to get memory usage
get_memory_usage() {
  local total=$(awk '/MemTotal/{print $2}' /proc/meminfo)
  local available=$(awk '/MemAvailable/{print $2}' /proc/meminfo)
  local used=$((total - available))
  local percent=$(echo "scale=2; ($used / $total) * 100" | bc)
  local total_gb=$(echo "scale=2; $total / 1024 / 1024" | bc)
  local available_gb=$(echo "scale=2; $available / 1024 / 1024" | bc)
  echo "${percent}% (${available_gb} GB free / ${total_gb} GB total)"
}

# Function to get disk usage
get_disk_usage() {
  local output=$(df -h | grep "^${DISK_PATH}" | awk '{print $2, $3, $4, $5}')
  local total=$(echo "$output" | awk '{print $1}')
  local used=$(echo "$output" | awk '{print $2}')
  local available=$(echo "$output" | awk '{print $3}')
  local percent=$(echo "$output" | awk '{print $4}' | sed 's/%//')
  echo "${percent}% (${available} free / ${total} total)"
}

# Function to get network statistics
get_network_stats() {
  local rx_bytes_initial=$(awk "/${NETWORK_INTERFACE}/ {print \$2}" /proc/net/dev)
  local tx_bytes_initial=$(awk "/${NETWORK_INTERFACE}/ {print \$10}" /proc/net/dev)
  sleep "$UPDATE_INTERVAL"
  local rx_bytes_final=$(awk "/${NETWORK_INTERFACE}/ {print \$2}" /proc/net/dev)
  local tx_bytes_final=$(awk "/${NETWORK_INTERFACE}/ {print \$10}" /proc/net/dev)

  local rx_diff=$((rx_bytes_final - rx_bytes_initial))
  local tx_diff=$((tx_bytes_final - tx_bytes_initial))

  local rx_mb=$(echo "scale=2; $rx_diff / 1024 / 1024" | bc)
  local tx_mb=$(echo "scale=2; $tx_diff / 1024 / 1024" | bc)

  echo "Sent: ${tx_mb} MB/s, Received: ${rx_mb} MB/s"
}

# Function to get uptime
get_uptime() {
  local uptime_seconds=$(cat /proc/uptime | awk '{print $1}')
  local days=$((uptime_seconds / 86400))
  local hours=$(( (uptime_seconds % 86400) / 3600 ))
  local minutes=$(( (uptime_seconds % 3600) / 60 ))
  local seconds=$(( uptime_seconds % 60 ))
  echo "${days} days, ${hours} hours, ${minutes} minutes, ${seconds} seconds"
}

# Main loop
while true; do
  clear_screen
  echo "--- System Monitor ---"
  echo "CPU Usage: $(get_cpu_usage)"
  echo "Memory Usage: $(get_memory_usage)"
  echo "Disk Usage (${DISK_PATH}): $(get_disk_usage)"
  echo "Network (${NETWORK_INTERFACE}): $(get_network_stats)"
  echo "Uptime: $(get_uptime)"
  echo "----------------------"
  sleep "$UPDATE_INTERVAL"
done