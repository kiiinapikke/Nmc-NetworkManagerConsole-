import psutil
import tkinter as tk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

root = tk.Tk()
root.title("NetworkManagerConsole")
root.geometry("500x400")
root.configure(background="#2b2b2b")

title_label = tk.Label(root, text="NetworkManager", font=("Arial", 16, "bold"), bg="#AFACAC")
title_label.pack(pady=10)

dwn_label = tk.Label(root, text="Download Speed:", font=("Arial", 16, "bold"), bg="#616060", fg="white")
dwn_label.pack(pady=10)

upl_label = tk.Label(root, text="Upload Speed:", font=("Arial", 16, "bold"), bg="#616060", fg="white")
upl_label.pack(pady=10)


prev_sent = psutil.net_io_counters().bytes_sent
prev_recv = psutil.net_io_counters().bytes_recv


upload_history = []
download_history = []
time_history = []
max_points = 20  


fig, ax = plt.subplots(figsize=(5, 2))
ax.set_title("Network Speed")
ax.set_xlabel("Time (s)")
ax.set_ylabel("Kb/s")
ax.set_ylim(0, 1000)
line_upload, = ax.plot([], [], label="Upload Speed", color="red")
line_download, = ax.plot([], [], label="Download Speed", color="green")
ax.legend()


canvas = FigureCanvasTkAgg(fig, master=root)
canvas.get_tk_widget().pack(pady=10)

def update_network():
    global prev_sent, prev_recv, upload_history, download_history, time_history

    counters = psutil.net_io_counters()
    sent = counters.bytes_sent
    recv = counters.bytes_recv

    upload_speed = (sent - prev_sent) * 8 / 1024
    download_speed = (recv - prev_recv) * 8 / 1024

    prev_sent = sent
    prev_recv = recv

    upl_label.config(text=f"Upload Speed: {upload_speed:.2f} Kb/s")
    dwn_label.config(text=f"Download Speed: {download_speed:.2f} Kb/s")

    
    upload_history.append(upload_speed)
    download_history.append(download_speed)
    time_history.append(len(time_history))

  
    upload_history = upload_history[-max_points:]
    download_history = download_history[-max_points:]
    time_history = time_history[-max_points:]

    line_upload.set_data(time_history, upload_history)
    line_download.set_data(time_history, download_history)
    ax.set_xlim(max(0, len(time_history)-max_points), len(time_history))
    ax.set_ylim(0, max(max(upload_history+download_history)+50, 100))

    canvas.draw()

    root.after(1003, update_network)

update_network()
root.mainloop()