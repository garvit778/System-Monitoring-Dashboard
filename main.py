import tkinter as tk
from tkinter import ttk
import monitor_functions
import time
import threading

class SystemMonitorApp:
    def __init__(self, root):
        self.root = root
        root.title("System Monitor")
        root.geometry("400x200")  # Set the initial window size
        root.resizable(False, False)  # Prevent resizing

        # --- Frames ---
        self.data_frame = ttk.Frame(root, padding="10")
        self.data_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # --- Labels and Variables ---
        ttk.Label(self.data_frame, text="CPU Usage:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        self.cpu_var = tk.StringVar()
        ttk.Label(self.data_frame, textvariable=self.cpu_var).grid(row=0, column=1, sticky=tk.W, padx=5, pady=5)

        ttk.Label(self.data_frame, text="Memory Usage:").grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)
        self.mem_var = tk.StringVar()
        ttk.Label(self.data_frame, textvariable=self.mem_var).grid(row=1, column=1, sticky=tk.W, padx=5, pady=5)

        ttk.Label(self.data_frame, text="Disk Usage:").grid(row=2, column=0, sticky=tk.W, padx=5, pady=5)
        self.disk_var = tk.StringVar()
        ttk.Label(self.data_frame, textvariable=self.disk_var).grid(row=2, column=1, sticky=tk.W, padx=5, pady=5)

        ttk.Label(self.data_frame, text="Network:").grid(row=3, column=0, sticky=tk.W, padx=5, pady=5)
        self.net_var = tk.StringVar()
        ttk.Label(self.data_frame, textvariable=self.net_var).grid(row=3, column=1, sticky=tk.W, padx=5, pady=5)

        ttk.Label(self.data_frame, text="Uptime:").grid(row=4, column=0, sticky=tk.W, padx=5, pady=5)
        self.uptime_var = tk.StringVar()
        ttk.Label(self.data_frame, textvariable=self.uptime_var).grid(row=4, column=1, sticky=tk.W, padx=5, pady=5)

        # --- Configure Grid Weights ---  Make the labels expand
        self.data_frame.columnconfigure(1, weight=1)

        # --- Update Function (run in a thread) ---
        self.running = True
        self.update_thread = threading.Thread(target=self.update_data)
        self.update_thread.start()

    def update_data(self):
        while self.running:
            try:
                cpu_usage = monitor_functions.get_cpu_usage()
                mem_usage = monitor_functions.get_memory_usage()
                disk_usage = monitor_functions.get_disk_usage()
                network_stats = monitor_functions.get_network_stats()
                uptime = monitor_functions.get_uptime()

                self.cpu_var.set(cpu_usage)
                self.mem_var.set(mem_usage)
                self.disk_var.set(disk_usage)
                self.net_var.set(network_stats)
                self.uptime_var.set(uptime)
            except Exception as e:
                print(f"Error updating data: {e}")
            time.sleep(2)

    def stop(self):
        self.running = False
        self.update_thread.join()

    def close_window(self):  # Add this function
        self.stop()
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = SystemMonitorApp(root)
    root.protocol("WM_DELETE_WINDOW", app.close_window)  # Use the new function
    root.mainloop()
